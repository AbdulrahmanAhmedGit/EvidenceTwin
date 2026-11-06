"""Durable exploratory review workflow. Model output is never a verified fact."""
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from pathlib import Path
import json
import fcntl
import hashlib
from werkzeug.exceptions import Conflict, ServiceUnavailable
from .store import Store, now, new_id
from .provider import ROLES, Review, CrossReview, Judgment, validate_references, PROMPTS

LIMITATIONS = [
    'Exploratory AI interpretations have not been independently scientifically verified.',
    'Source authenticity and source content have not been verified; URLs are supplied metadata only.',
    'No deterministic statistical tests or neutral visualization were generated.',
    'Reviewers may share a model and systematic errors. Agreement does not establish scientific truth.',
]

class StaleJob(Exception):
    pass

class Workflow:
    def __init__(self, store: Store, provider, workers: int, queue_limit: int):
        self.store, self.provider = store, provider
        self.process_lock = (store.root / "worker.lock").open("a+")
        try:
            fcntl.flock(self.process_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.process_lock.close()
            raise RuntimeError("This workspace already has an active backend process; use a single application worker.") from None
        self.pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix='evidencetwin')
        self.slots = BoundedSemaphore(queue_limit)
        self.futures = {}
        self.recover()

    def recover(self):
        # Never silently replay billable model calls after a process restart.
        for record in self.store.all('analysis'):
            if record['analysis']['status'] in ('queued','running'):
                record['analysis'].update(status='failed',error='The application stopped during processing. Retry explicitly to start a new attempt.',actions={'retry':True,'cancel':False})
                self.store.event(record,'workflow','interrupted','failed')
                self.store.put('analysis',record)

    def submit(self, record: dict):
        if not self.provider.configured:
            raise ServiceUnavailable('Review provider is not configured.')
        if not self.slots.acquire(blocking=False):
            raise ServiceUnavailable('The local review queue is full.')
        try:
            with self.store.lock:
                record['attempt'] = new_id()
                record['analysis'].update(status='queued',stage='Waiting for an available local worker',actions={'retry':False,'cancel':True})
                record['analysis'].pop('error',None)
                self.store.event(record,'workflow','analysis_queued',attempt=record['attempt'],
                                 provider=getattr(self.provider,'name','Ollama'),model=self.provider.model,
                                 promptHashes={path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in PROMPTS.glob('*.md')})
                self.store.put('analysis',record)
                future = self.pool.submit(self.run,record['id'],record['attempt'],self.provider)
                self.futures[record['id']] = future
                future.add_done_callback(lambda f: self.release(record['id'], f))
        except BaseException:
            self.slots.release()
            raise

    def release(self, record_id, future):
        self.slots.release()
        with self.store.lock:
            if self.futures.get(record_id) is future:
                self.futures.pop(record_id,None)

    def update(self, record_id: str, attempt: str, change):
        with self.store.lock:
            try:
                r = self.store.get('analysis',record_id)
            except Exception:
                raise StaleJob() from None
            if r['attempt'] != attempt or r['analysis']['status'] == 'cancelled':
                raise StaleJob()
            change(r)
            self.store.put('analysis',r)
            return r

    def stage(self, record_id, attempt, label):
        def change(r):
            r['analysis'].update(status='running',stage=label)
            r['analysis'].setdefault('startedAt',now())
            self.store.event(r,'workflow',label,'running')
        return self.update(record_id,attempt,change)

    def cancel(self, record_id: str):
        with self.store.lock:
            r = self.store.get('analysis',record_id)
            if r['analysis']['status'] not in ('queued','running'):
                raise Conflict()
            r['analysis'].update(status='cancelled',stage='Cancelled',actions={'retry':True,'cancel':False})
            self.store.event(r,'workflow','analysis_cancelled')
            self.store.put('analysis',r)
        # In-flight HTTP may finish, but attempt/state checks discard its results.

    def call(self, record_id, attempt, role, packet, images, schema, reports, provider):
        self.stage(record_id,attempt,'Review: '+role.replace('_',' '))
        try:
            reply = provider.chat(role,packet,images,schema)
            data = schema.model_validate(reply['data']).model_dump()
            validate_references(role,data,packet,reports)
            def save(r):
                if role in ROLES:
                    name,key,_,_ = ROLES[role]
                    summary = data['overall_assessment']
                    findings = [f['title']+': '+f['observation'] for f in data['findings']]
                    refs = sorted({ref for f in data['findings'] for ref in f['evidence_refs']} | {ref for c in data['claim_assessments'] for ref in c['evidence_refs']})
                    status = data['review_status']
                else:
                    name = 'Cross-Reviewer' if role == 'cross_reviewer' else 'Evidence Judge'
                    summary = data.get('overall_quality_assessment') or 'AI adjudication: '+data['overall_verdict'].replace('_',' ')
                    findings = [c['description'] for c in data['critiques']] if role == 'cross_reviewer' else data['key_findings']
                    refs = sorted({ref for c in data.get('critiques',[]) for ref in c['evidence_refs']} | {ref for c in data.get('claim_results',[]) for ref in c['supporting_evidence_refs']+c['contradicting_evidence_refs']})
                    status = data.get('review_status','completed')
                item = {'id':role,'role':name,'phase':'independent' if role in ROLES else 'cross-review' if role=='cross_reviewer' else 'judge',
                        'status':status,'summary':summary,'findings':findings,'citations':refs,
                        'model':reply['model'],'provider':getattr(provider,'name','Ollama'),'uncertainty':data['limitations'],
                        'report':{'output':data,'usage':reply.get('usage',{}),'classification':'AI interpretation; not scientific verification'}}
                if role in ROLES:
                    item.update(roleKey=key,independentExecution=True,claims=[c['claim_id'] for c in data['claim_assessments']])
                r['reviews'] = [x for x in r['reviews'] if x['id'] != role]+[item]
                r['raw'][role] = data
                self.store.event(r,role,'review_completed',status)
            self.update(record_id,attempt,save)
            return data
        except StaleJob:
            raise
        except Exception:
            def failure(r):
                role_name = ROLES[role][0] if role in ROLES else role.replace('_',' ').title()
                r['reviews'].append({'id':role,'role':role_name,'phase':'independent' if role in ROLES else 'cross-review' if role=='cross_reviewer' else 'judge',
                                     'status':'failed','summary':'The provider failed or its structured response did not pass validation.',
                                     'findings':[],'citations':[]})
                self.store.event(r,role,'review_failed','failed')
            self.update(record_id,attempt,failure)
            return None

    def run(self, record_id: str, attempt: str, provider):
        try:
            r = self.stage(record_id,attempt,'Preparing supplied evidence')
            packet = r['packet']
            images = [self.store.uploads/record_id/f['id'] for f in r['files'] if f['mediaType'].startswith('image/')]
            reports = {}
            roles = list(ROLES) if r['metadata']['reviewDepth']=='council' else ['visual_analyst']
            for role in roles:
                # Every initial call receives the same packet with no other reviews.
                data = self.call(record_id,attempt,role,packet,images,Review,{},provider)
                if data is not None: reports[role] = data
            if not reports:
                raise RuntimeError('No valid reviews')
            cross = judge = None
            if len(reports)==4:
                cross_packet = {**packet,'reviewer_reports':reports}
                cross = self.call(record_id,attempt,'cross_reviewer',cross_packet,images,CrossReview,reports,provider)
                if cross is not None:
                    judge_packet = {**cross_packet,'cross_review':cross}
                    judge = self.call(record_id,attempt,'evidence_judge',judge_packet,images,Judgment,reports,provider)
            def finish(r):
                a = r['analysis']
                a.update(status='completed_with_limitations',stage='Exploratory review complete',actions={'retry':False,'cancel':False})
                a['reviewSummary'] = [{'role':v['role'],'status':v['status'],'summary':v['summary']} for v in r['reviews']]
                a['findings'] = [{'kind':'interpretation','text':f['title']+': '+f['observation'],'citations':f['evidence_refs'],'sourceVerified':False}
                                 for report in reports.values() for f in report['findings']]
                a['limitations'] = list(dict.fromkeys(r['packet']['limitations']+[l for v in reports.values() for l in v['limitations']+v['missing_information']]))
                if len(reports) != len(roles): a['limitations'].append('One or more initial reviewers failed; cross-review and judging were not performed.')
                if judge:
                    # Frontend's verdict badge does not distinguish model adjudication
                    # from verification: retain the proposed verdict only in Judge report.
                    a['suggestedInterpretation'] = 'AI-generated suggested wording (unverified): '+judge['recommended_wording']
                    a['limitations'].extend(judge['limitations'])
                a['assessment'] = 'not_evaluated'
                if cross:
                    r['disagreements'] = [{'id':new_id(),'claim':d['description'],'positions':d['agent_ids'],'status':'unresolved',
                                           'resolution':'Additional information needed: '+'; '.join(d['required_information'])} for d in cross['unresolved_disagreements']]
                if len(roles)==4 and (cross is None or judge is None):
                    a['limitations'].append('Full Council adjudication is incomplete. Inspect reviewer states.')
                self.store.event(r,'workflow','analysis_completed_with_limitations')
                r['report'] = self.report(r)
            self.update(record_id,attempt,finish)
        except StaleJob:
            return
        except Exception:
            try:
                def fail(r):
                    r['analysis'].update(status='failed',error='No usable review was produced. Check provider configuration and retry.',actions={'retry':True,'cancel':False})
                    self.store.event(r,'workflow','analysis_failed','failed')
                self.update(record_id,attempt,fail)
            except StaleJob:
                pass

    def report(self, r):
        a = r['analysis']
        sections = [
            {'id':'summary','title':'Executive summary','body':'Exploratory AI review of supplied evidence. This report is not independent scientific verification.'},
            {'id':'claim','title':'Original claims','body':'\n'.join(a['claims'])},
            {'id':'evidence','title':'Submitted evidence','body':'\n'.join(e['id']+': '+e['description'] for e in r['packet']['evidence'])},
            {'id':'provenance','title':'Source and provenance','body':'All sources and files are user supplied and unverified. Source content was not fetched.'},
        ]
        for v in r['reviews']:
            sections.append({'id':v['id'],'title':v['role']+' — AI interpretation','body':v['summary']+'\n'+'\n'.join(v['findings'])})
        sections.extend([
            {'id':'limitations','title':'Limitations','body':'\n'.join(a['limitations'])},
            {'id':'reproducibility','title':'Reproducibility','body':'Input hashes, actual model names, structured outputs and execution events are retained. Same-provider isolated calls do not establish independent scientific confirmation.'},
        ])
        return {'permissions':{'reportJson':True},'report':{'title':a['title'],'generatedAt':now(),'version':'1','reproducibility':'See evidence contract and audit trail.'},'sections':sections}

    def shutdown(self):
        self.pool.shutdown(wait=True,cancel_futures=True)
        self.process_lock.close()
