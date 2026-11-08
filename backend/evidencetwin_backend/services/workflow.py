"""Durable exploratory review workflow. Model output is never a verified fact."""
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from pathlib import Path
from copy import copy
import json
import fcntl
import hashlib
from werkzeug.exceptions import Conflict, ServiceUnavailable
from .store import Store, now, new_id
from .provider import ROLES, Review, CrossReview, Judgment, validate_references, PROMPTS
from ..science.processing import process_record, prepare_packet
from ..science.datasets import query_dataset
from ..science.coverage import format_coverage

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

    def submit(self, record: dict, related=None):
        if not self.provider.configured:
            raise ServiceUnavailable('Review provider is not configured.')
        if not self.slots.acquire(blocking=False):
            raise ServiceUnavailable('The local review queue is full.')
        try:
            with self.store.lock:
                record['attempt'] = new_id()
                record['promptSnapshots'] = {path.name: path.read_text() for path in PROMPTS.glob('*.md')}
                record['analysis'].update(status='queued',stage='Waiting for an available local worker',actions={'retry':False,'cancel':True})
                record['analysis'].pop('error',None)
                self.store.event(record,'workflow','analysis_queued',attempt=record['attempt'],
                                 provider=getattr(self.provider,'name','Ollama'),model=self.provider.model,
                                 promptHashes={name:hashlib.sha256(text.encode()).hexdigest() for name,text in record['promptSnapshots'].items()})
                self.store.put_many([('analysis', record), *(related or [])])
                provider = copy(self.provider)
                provider.prompt_snapshots = record['promptSnapshots']
                future = self.pool.submit(self.run,record['id'],record['attempt'],provider)
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
        reply = None
        try:
            reply = provider.chat(role,packet,images,schema)
            data = schema.model_validate(reply['data']).model_dump()
            query_log = []
            query_request = None
            if role in ROLES and data.get('requested_queries'):
                query_request = {'output': data, 'rawOutput': reply.get('rawOutput'), 'usage': reply.get('usage', {})}
                record = self.store.get('analysis', record_id)
                for index, query in enumerate(data['requested_queries']):
                    try:
                        selected_dataset = record.get('dataset')
                        uploaded_id = next((f['id'] for f in record['files'] if f['mediaType'] in ('text/csv', 'application/json')), None)
                        processing = record.get('processing', {})
                        source_tables = {source.get('evidenceId', 'retrieved-source'): source.get('dataset')
                                         for source in processing.get('sources', [processing['source']] if processing.get('source') else [])}
                        if query.get('evidence_id') in source_tables:
                            selected_dataset = source_tables[query['evidence_id']]
                        elif query.get('evidence_id') not in (None, uploaded_id):
                            raise ValueError('Unknown dataset evidence identifier.')
                        if selected_dataset is None:
                            raise ValueError('No parsed structured dataset is available for this evidence identifier.')
                        outcome = query_dataset(selected_dataset, query['filters'], query['limit'])
                        outcome['evidenceId'] = query.get('evidence_id') or uploaded_id
                    except ValueError as error:
                        outcome = {'error': str(error), 'filters': query['filters']}
                    outcome['id'] = f'{role}-query-{index + 1}'
                    query_log.append(outcome)
                packet = {**packet, 'requested_query_results': query_log,
                          'evidence': packet['evidence'] + [{'id': q['id'], 'kind': 'dataset_query', 'description': json.dumps(q['filters'], ensure_ascii=False), 'verified': False} for q in query_log]}
                reply = provider.chat(role, packet, images, schema)
                data = schema.model_validate(reply['data']).model_dump()
                if data.get('requested_queries'):
                    raise ValueError('Evidence query round limit exceeded.')
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
                        'report':{'output':data,'usage':reply.get('usage',{}),'rawOutput':reply.get('rawOutput'),
                                  'queries':query_log,'queryRequest':query_request,'classification':'AI interpretation; not scientific verification'}}
                if role in ROLES:
                    item.update(roleKey=key,independentExecution=True,claims=[c['claim_id'] for c in data['claim_assessments']])
                r['reviews'] = [x for x in r['reviews'] if x['id'] != role]+[item]
                r['raw'][role] = data
                r.setdefault('agentInputs', {})[role] = packet
                self.store.event(r,role,'review_completed',status)
            self.update(record_id,attempt,save)
            return data
        except StaleJob:
            raise
        except Exception as error:
            last_output = getattr(error, 'raw_output', None) or (reply or {}).get('rawOutput')
            def failure(r):
                role_name = ROLES[role][0] if role in ROLES else role.replace('_',' ').title()
                r['reviews'].append({'id':role,'role':role_name,'phase':'independent' if role in ROLES else 'cross-review' if role=='cross_reviewer' else 'judge',
                                     'status':'failed','summary':'The provider failed or its structured response did not pass validation.',
                                     'findings':[],'citations':[]})
                self.store.event(r,role,'review_failed','failed')
                if last_output is not None:
                    r.setdefault('failedOutputs', {}).setdefault(role, []).append({
                        'rawOutput': last_output, 'classification': 'Last received model text before an unconfirmed or invalid review. Not accepted as a scientific finding.'})
            self.update(record_id,attempt,failure)
            return None

    def run(self, record_id: str, attempt: str, provider):
        try:
            r = self.stage(record_id,attempt,'Preparing supplied evidence')
            processing = process_record(r, self.store.uploads, retrieve=True)
            packet = prepare_packet(r, processing)
            def prepared(record):
                record['processing'] = processing
                record['packet'] = packet
                self.store.event(record, 'evidence', 'complete_evidence_prepared', version=processing['version'],
                                 queries=[q for table in processing['datasets'] for q in table['queries']])
            r = self.update(record_id, attempt, prepared)
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
                reviewed = self.store.get('analysis', record_id)
                requested = [q for value in reviewed.get('agentInputs', {}).values() for q in value.get('requested_query_results', [])]
                packet = {**packet, 'reviewer_query_results': requested, 'evidence': packet['evidence'] + [
                    {'id': q['id'], 'kind': 'dataset_query', 'description': json.dumps(q['filters'], ensure_ascii=False), 'verified': False} for q in requested]}
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
                grouped = {}
                for role, report in reports.items():
                    for item in report.get('limitation_records', []):
                        key = (item['category'], item['check'], tuple(sorted(item['evidence_refs'])))
                        if key not in grouped:
                            grouped[key] = {'id': 'review-limit-' + new_id(), 'category': item['category'],
                                            'check': item['check'], 'importance': item['importance'],
                                            'explanation': item['explanation'], 'nextStep': item['next_step'],
                                            'evidenceRefs': item['evidence_refs'], 'reportedBy': [], 'variants': [],
                                            'classification': 'Reviewer-reported limitation; not an independently established fact'}
                        grouped[key]['reportedBy'].append(role)
                        priority = {'blocking': 0, 'important': 1, 'context': 2}
                        if priority[item['importance']] < priority[grouped[key]['importance']]:
                            grouped[key]['importance'] = item['importance']
                        grouped[key]['variants'].append({'role': role, 'explanation': item['explanation'], 'cause': item['cause']})
                r['processing']['limitations'].extend(grouped.values())
                r['processing']['limitations'].sort(key=lambda item: {'blocking':0,'important':1,'context':2}[item['importance']])
                comparisons = [c for table in processing['datasets'] for c in table['comparisons']]
                for comparison in comparisons:
                    left, right = comparison['observations']
                    relation = 'equal to' if comparison['relation'] == 'equal' else comparison['relation'] + ' than'
                    a['findings'].insert(0, {'kind': 'calculation', 'text': f"{left['label']} ({left['value']}) is {relation} {right['label']} ({right['value']}) in the submitted {comparison['year']} indicator. Difference {comparison['difference']} {comparison['differenceUnit']}. {comparison['scope']}",
                                            'citations': [comparison['id']], 'sourceVerified': False})
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
                    r['analysis'].update(status='failed',error='No usable review was produced. Your evidence is preserved. Try again later or contact your pilot operator.',actions={'retry':True,'cancel':False})
                    self.store.event(r,'workflow','analysis_failed','failed')
                self.update(record_id,attempt,fail)
            except StaleJob:
                pass

    def report(self, r):
        a = r['analysis']
        processing = r.get('processing', {})
        comparisons = [c for table in processing.get('datasets', []) for c in table['comparisons']]
        quantitative = []
        for table in processing.get('datasets', []):
            for c in table['comparisons']:
                left, right = c['observations']
                quantitative.append(f"{c['indicator']} · {c['year']}\n{left['label']}: {left['value']} (row {left['rowNumber']})\n{right['label']}: {right['value']} (row {right['rowNumber']})\nDifference: {c['difference']} {c['differenceUnit']}\nRatio: {c['ratio'] or 'undefined (zero denominator)'}\n{c['method']}\n{c['scope']}")
        sources = processing.get('sources', [processing['source']] if processing.get('source') else [])
        provenance = '\n\n'.join(source['url'] + '\nRetrieval ' + source['status'].replace('_', ' ') + '. ' + source.get('reason', '') +
                                   '\nAuthenticity unverified. Content assertions await independent verification.' for source in sources) or 'No supported source reference was supplied.'
        visual_review = next((review for review in r['reviews'] if review['id'] == 'visual_analyst'), None)
        visual_summary = (visual_review or {}).get('summary') or 'No completed visual-review explanation is available. Inspect the original chart and execution record.'
        sections = [
            {'id':'visual_summary','title':'Visual inspection — AI interpretation','body':visual_summary + '\n\nVisual concerns require supporting evidence and independent confirmation. Blind reconstruction was not performed; its approved blinding/rendering protocol remains unavailable.'},
            {'id':'summary','title':'Executive finding','body': ('The submitted dataset permits a reproducible descriptive comparison. See the exact observations and scope below.' if comparisons else 'No unambiguous automatic numerical comparison was established. Inspect the evidence selection and Council perspectives.') + '\nScientific claim assessment remains not evaluated. Model review and software execution are separately reported.'},
            {'id':'quantitative','title':'Reported values and calculations','body':'\n\n'.join(quantitative) or 'No supported descriptive calculation was performed.'},
            {'id':'claim','title':'Original claims','body':'\n'.join(a['claims'])},
            {'id':'evidence','title':'Submitted evidence','body':'\n'.join(f['name'] + ' — ' + f['mediaType'] for f in r['files'])},
            {'id':'provenance','title':'Source and provenance','body':provenance},
            {'id':'coverage','title':'Checks and evidence coverage','body':format_coverage(processing.get('coverage', []))},
        ]
        for v in r['reviews']:
            sections.append({'id':v['id'],'title':v['role']+' — AI interpretation','body':v['summary']+'\n'+'\n'.join(v['findings'])})
        sections.extend([
            {'id':'limitations','title':'Limitations and next steps','body':'\n\n'.join(
                ('AI reviewer concern. ' if item.get('classification') else '') + item['explanation'] + '\n' + item['nextStep']
                for item in processing.get('limitations', [])) or '\n'.join(a['limitations'])},
            {'id':'reproducibility','title':'Reproducibility','body':'Input hashes, actual model names, structured outputs and execution events are retained. Same-provider isolated calls do not establish independent scientific confirmation.'},
        ])
        return {'permissions':{'reportJson':True},'report':{'title':a['title'][:100],'generatedAt':now(),'version':'4','reproducibility':'Evidence processing ' + processing.get('version', 'legacy') + '. See exact row references, source snapshots, prompt snapshots, per-role inputs and raw outputs in the evidence and audit record.'},'sections':sections}

    def shutdown(self):
        self.pool.shutdown(wait=True,cancel_futures=True)
        self.process_lock.close()
