"""HTTP/application boundary for the single-workspace backend.

No source scraping, fabricated verification, gold-label evaluation or MCP server.
"""
import csv
from copy import deepcopy
from functools import wraps
import hashlib
from io import StringIO, BytesIO
import json
from pathlib import Path
import shutil
import warnings
from urllib.parse import urlsplit
from flask import current_app, jsonify, request, send_file
from pydantic import ValidationError
from PIL import Image
from werkzeug.exceptions import BadRequest, Conflict, NotFound, ServiceUnavailable, UnsupportedMediaType, UnprocessableEntity
from ..contracts.common import validate_contract
from ..contracts.analyses import AnalysisCreateMetadata, Analysis, AnalysisList
from ..contracts.inspection import SectionResponse, Dataset
from ..contracts.queries import AnalysisListQuery, ReportListQuery, BenchmarkListQuery, ComparisonQuery, DatasetQuery, ActivityQuery
from ..contracts.research import ComparisonResponse, ReportList, IntegrationList, BenchmarkList, BenchmarkResponse
from ..contracts.system import ActivityResponse, CapabilitiesResponse
from ..errors import not_implemented
from .store import Store, new_id, now
from .transports import make_provider
from .provider import OllamaProvider
from .ai_settings import AISettings
from .workflow import Workflow, LIMITATIONS
from .access import install_access, principal, owned, can_read, operator
from ..science.source_links import discover_sources
from .report_translation import ReportTranslations, install_report_translations

CASES = [
    {'id':'a1','title':'Truncated axis','sample':True,'sourceStatus':'unverified','columns':['Year','Reported percentage'],'rows':[['2021',42],['2023',40]],'limitations':['Illustrative input from project brief; original source not authenticated.','No sample sizes or uncertainty supplied. A two-percentage-point difference alone does not establish significance.']},
    {'id':'a2','title':'Causal framing','sample':True,'sourceStatus':'unverified','columns':['Group','Reported percentage'],'rows':[['Frequent social-media group',42.6],['Less frequent group',31.9]],'limitations':['Illustrative input from project brief; original source not authenticated.','Observational association alone does not establish causation.']},
    {'id':'a3','title':'Uncertainty presentation','sample':True,'sourceStatus':'unverified','columns':['Group','Reported percentage'],'rows':[['Grade 9',40.3],['Grade 10',39.7]],'limitations':['Illustrative input from project brief; original source not authenticated.','Exact interval bounds unavailable. Interval overlap alone cannot establish significance.']},
]

class Runtime:
    def __init__(self, app):
        self.store = Store(app.config['DATA_DIRECTORY'])
        self.ai_settings=AISettings(self.store.root,app.config,self.store.lock)
        self.provider = app.config.get('REVIEW_PROVIDER') or make_provider(self.ai_settings.effective())
        self.workflow = Workflow(self.store,self.provider,app.config['WORKERS'],app.config['QUEUE_LIMIT'])
        self.translations = ReportTranslations(self.store, app.config)

    def get_ai_settings(self):
        operator()
        return jsonify(self.ai_settings.public())

    def save_ai_settings(self):
        operator()
        if request.mimetype!='application/json': raise UnsupportedMediaType()
        with self.store.lock:
            provider=self.ai_settings.save(request.get_json())
            self.provider=provider
            self.workflow.provider=provider
        return jsonify(self.ai_settings.public())

    def test_ai_settings(self):
        operator()
        # Test saved configuration only; never echo a key or make a paid generation.
        with self.store.lock:
            provider=self.provider
        ok=provider.configured and provider.probe()
        return jsonify({'status':'reachable' if ok else 'failed',
                        'message':'model_found' if ok else 'model_unconfirmed','checkedAt':now()})

    def response(self, schema, payload):
        return jsonify(validate_contract(schema,payload))

    def query(self, schema, defaults=None):
        if any(len(request.args.getlist(key)) != 1 for key in request.args): raise UnprocessableEntity()
        return validate_contract(schema,{**(defaults or {}),**request.args.to_dict()})

    def record(self, analysis_id):
        return owned(self.store,'analysis',analysis_id)

    def records(self, kind='analysis'):
        return [r for r in self.store.all(kind) if can_read(r)]

    def page(self, rows, q, title='title', verdict='assessment'):
        text = q.get('search','').casefold()
        rows = [r for r in rows if text in (r.get(title,'')+' '+r.get('source','')+' '+r.get('summary','')).casefold()]
        for key,field in [('status','status'),('mode','mode'),('verdict',verdict)]:
            if q.get(key): rows = [r for r in rows if r.get(field)==q[key]]
        if q.get('from'): rows = [r for r in rows if r['createdAt'][:10]>=q['from']]
        if q.get('to'): rows = [r for r in rows if r['createdAt'][:10]<=q['to']]
        sort = q.get('sort') or 'createdAt:desc'
        field,direction = sort.split(':')
        rows.sort(key=lambda r:str(r.get(field,'')).casefold(),reverse=direction=='desc')
        page, size = q.get('page',1),q.get('pageSize',10)
        return {'items':rows[(page-1)*size:page*size],'total':len(rows),'page':page,'pageSize':size}

    def summary(self,r):
        a = r['analysis']
        keys = ('id','title','createdAt','status','mode','assessment')
        return {**({'researchCaseId':r['researchCaseId']} if r.get('researchCaseId') else {}), **{k:a[k] for k in keys if k in a},'source':r['metadata']['source'],
                'reportAvailable':r.get('report') is not None}

    def build_record(self, base=None):
        if request.mimetype!='multipart/form-data': raise UnsupportedMediaType()
        if set(request.form)-{'metadata','retainedFiles'} or 'metadata' not in request.form or any(len(request.form.getlist(k))!=1 for k in request.form) or set(request.files)-{'files'}: raise UnprocessableEntity()
        metadata = validate_contract(AnalysisCreateMetadata,json.loads(request.form['metadata']))
        if metadata['mode']!='exploratory': raise UnprocessableEntity()
        if metadata['claim'] != metadata['claims'][0] or len(set(metadata['claims']))!=len(metadata['claims']): raise UnprocessableEntity()
        if metadata['url']:
            u = urlsplit(metadata['url'])
            if u.scheme not in ('http','https') or not u.hostname or u.username or u.password: raise UnprocessableEntity()
        files = request.files.getlist('files')
        if len(files)>10: raise UnprocessableEntity()
        record_id = new_id()
        directory = self.store.uploads/record_id
        directory.mkdir(mode=0o700)
        saved, dataset, hashes = [],None,set()
        try:
            if base:
                retained = json.loads(request.form.get('retainedFiles', '[]'))
                if not isinstance(retained, list) or len(set(retained)) != len(retained) or any(not isinstance(x, str) for x in retained):
                    raise UnprocessableEntity()
                if set(retained) - {f['id'] for f in base['files']}:
                    raise UnprocessableEntity()
                for original in base['files']:
                    if original['id'] not in retained:
                        continue
                    shutil.copyfile(self.store.uploads/base['id']/original['id'], directory/original['id'])
                    (directory/original['id']).chmod(0o600)
                    saved.append(deepcopy(original))
                    hashes.add(original['sha256'])
                    if original['mediaType'] in ('text/csv', 'application/json'):
                        dataset = deepcopy(base['dataset'])
            elif request.form.get('retainedFiles') not in (None, '[]'):
                raise UnprocessableEntity()
            if len(saved) + len(files) > 10:
                raise UnprocessableEntity()
            for file in files:
                # Store under generated IDs, retaining the original Unicode name.
                # Reject path/control characters instead of losing Arabic names.
                name = file.filename or ''
                if len(name)>240 or any(ord(c)<32 for c in name) or '/' in name or '\\' in name:
                    raise UnprocessableEntity()
                ext = Path(name).suffix.lower()
                formats = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.csv':'text/csv','.json':'application/json','.pdf':'application/pdf'}
                if not name or ext not in formats: raise UnsupportedMediaType()
                data = file.stream.read(20*1024*1024+1)
                if not data or len(data)>20*1024*1024: raise UnprocessableEntity()
                digest = hashlib.sha256(data).hexdigest()
                if digest in hashes: raise UnprocessableEntity()
                hashes.add(digest)
                media = formats[ext]
                if media.startswith('image/'):
                    with warnings.catch_warnings():
                        warnings.simplefilter('error',Image.DecompressionBombWarning)
                        try:
                            with Image.open(BytesIO(data)) as image:
                                if image.width*image.height>16_000_000 or image.format not in ('PNG','JPEG','WEBP') or Image.MIME[image.format]!=media: raise UnprocessableEntity()
                                image.verify()
                        except (OSError, SyntaxError, ValueError):
                            raise UnprocessableEntity() from None
                elif ext=='.pdf':
                    if not data.startswith(b'%PDF-'): raise UnprocessableEntity()
                elif ext=='.json':
                    if dataset is not None: raise UnprocessableEntity()
                    parsed=json.loads(data.decode('utf-8-sig'))
                    if not isinstance(parsed,dict) or set(parsed)-{'columns','rows','variables','notes'}: raise UnprocessableEntity()
                    dataset=validate_contract(Dataset,parsed)
                    if len(dataset['columns'])>100 or len(set(dataset['columns']))!=len(dataset['columns']) or any(not col.strip() for col in dataset['columns']): raise UnprocessableEntity()
                    if any(len(str(cell))>10000 for row in dataset['rows'] for cell in row): raise UnprocessableEntity()
                else:
                    if dataset is not None: raise UnprocessableEntity()
                    try:
                        rows = list(csv.reader(StringIO(data.decode('utf-8-sig'))))
                    except (UnicodeError,csv.Error): raise UnprocessableEntity() from None
                    if not rows or not rows[0] or len(rows)>5001 or len(rows[0])>100 or len(set(rows[0]))!=len(rows[0]) or any(not c.strip() for c in rows[0]) or any(len(row)!=len(rows[0]) for row in rows): raise UnprocessableEntity()
                    if any(len(c)>10000 for row in rows for c in row): raise UnprocessableEntity()
                    dataset = {'columns':rows[0],'rows':rows[1:],'notes':['User-supplied CSV; values are retained as supplied strings. No source verification or inference performed.']}
                file_id = new_id()
                (directory/file_id).write_bytes(data)
                (directory/file_id).chmod(0o600)
                saved.append({'id':file_id,'name':name,'size':len(data),'mediaType':media,'status':'accepted','sha256':digest})
            if sum(f['size'] for f in saved)>64*1024*1024: raise UnprocessableEntity()
            if len([f for f in saved if f['mediaType'].startswith('image/')])>5: raise UnprocessableEntity()
            if metadata.get('caseId'):
                case = next(c for c in CASES if c['id']==metadata['caseId'])
                if dataset is None: dataset = {**{k:case[k] for k in ('columns','rows')},'notes':['Illustrative educational values from the project brief; not verified research observations.']}
            evidence = [{'id':f['id'],'description':f['name'],'kind':'uploaded_file','sha256':f['sha256'],'mediaType':f['mediaType'],'verified':False} for f in saved]
            evidence.append({'id':'study','description':'User-supplied source and study metadata','kind':'metadata','verified':False})
            if dataset: evidence.append({'id':'dataset','description':'Supplied dataset values','kind':'dataset','verified':False})
            packet = {'case_id':record_id,'claims':[{'id':f'claim-{i+1}','text':c} for i,c in enumerate(metadata['claims'])],
                      'evidence':evidence,'study':{k:metadata[k] for k in ('source','url','studyDate','studyDesign','population','uncertainty','context')},
                      'limitations':LIMITATIONS+(['PDF attachments are retained but their contents were not extracted or sent to the model.'] if any(f['mediaType']=='application/pdf' for f in saved) else []),
                      'attached_images':[{'image_index':i,'evidence_id':f['id'],'filename':f['name']} for i,f in enumerate(f for f in saved if f['mediaType'].startswith('image/'))],
                      'educational_case':metadata.get('caseId'),
                      'neutral_visualization':None,'scientific_pipeline':{'source_verification':'unavailable','dataset_validation':'transport_shape_only','statistical_checks':'unavailable','blind_optics':'unavailable','neutral_twin':'unavailable'}}
            if metadata.get('caseId'):
                packet['limitations'].append('An explicitly selected educational example is included; sample values are not live verified research data.')
            if dataset:
                # Complete rows stay in the record and original file. The worker
                # prepares exact, auditable selections instead of a first-N excerpt.
                packet['dataset'] = {**dataset,'rows':[],'totalRows':len(dataset['rows']),'contextTruncated':bool(dataset['rows']),
                                     'selection':'Not yet selected. Complete-table processing runs before Council review.'}
            record = {'id':record_id,'ownerId':principal()['id'],'metadata':metadata,'files':saved,'packet':packet,'dataset':dataset,'reviews':[],'raw':{},'events':[],
                      'disagreements':[],'report':None,'analysis':{'id':record_id,'title':metadata['source'] or metadata['claim'][:100],
                      'createdAt':now(),'status':'queued','mode':'exploratory','claim':metadata['claim'],'claims':metadata['claims'],
                      'limitations':packet['limitations'],'findings':[],'sourceStatus':'unverified'}}
            self.store.event(record,'uploads','files_accepted',count=len(saved))
            return record
        except BaseException:
            shutil.rmtree(directory,ignore_errors=True)
            raise

    def create_analysis(self):
        if not self.provider.configured: raise ServiceUnavailable()
        record = self.build_record()
        try:
            if not record['files'] and not record['metadata'].get('caseId') and not discover_sources(record['metadata'])['candidates']:
                raise UnprocessableEntity()
            self.workflow.submit(record)
        except BaseException:
            shutil.rmtree(self.store.uploads/record['id'], ignore_errors=True)
            raise
        return jsonify({'id':record['id']}),202

    def list_analyses(self):
        return self.response(AnalysisList,self.page([self.summary(r) for r in self.records()],self.query(AnalysisListQuery)))

    def get_analysis(self,analysis_id):
        r = self.record(analysis_id)
        payload = {**r['analysis'], 'reportAvailable': r.get('report') is not None}
        if r.get('researchCaseId'): payload['researchCaseId'] = r['researchCaseId']
        return self.response(Analysis,payload)

    def delete_analysis(self,analysis_id):
        with self.store.lock:
            r = self.record(analysis_id)
            if r.get('researchCaseId'): raise Conflict()
            if r['analysis']['status'] in ('queued','running'): raise Conflict()
            self.store.delete('analysis',analysis_id)
            shutil.rmtree(self.store.uploads/analysis_id,ignore_errors=True)
        return '',204

    def retry_analysis(self,analysis_id):
        with self.store.lock:
            r = self.record(analysis_id)
            if r['analysis']['status'] not in ('failed','cancelled'): raise Conflict()
            r.setdefault('attemptHistory',[]).append(deepcopy({key:r[key] for key in ('attempt','analysis','reviews','raw','disagreements','report','packet','processing','promptSnapshots','agentInputs','failedOutputs') if key in r}))
            r.update(reviews=[],raw={},disagreements=[],report=None)
            r.pop('processing', None)
            r.pop('agentInputs', None)
            r.pop('failedOutputs', None)
            a = r['analysis']
            a.update(findings=[],limitations=r['packet']['limitations'])
            for key in ('assessment','suggestedInterpretation','reviewSummary','startedAt'): a.pop(key,None)
            self.workflow.submit(r)
        return jsonify({}),202

    def cancel_analysis(self,analysis_id):
        self.record(analysis_id)
        self.workflow.cancel(analysis_id)
        return jsonify({}),202

    def get_analysis_evidence(self,analysis_id):
        r = self.record(analysis_id)
        m = r['metadata']
        source = {'id':'study','title':m['source'] or 'User-supplied source','status':'unverified',
                  'checked':'Metadata accepted only. The URL was not fetched and authenticity was not checked.','limitations':LIMITATIONS[1:2]}
        retrieval = r.get('processing', {}).get('source')
        if retrieval:
            source.update(checked='Retrieval ' + retrieval['status'] + '. ' + retrieval.get('reason', '') + ' Authenticity remains unverified.',
                          limitations=['Retrieval does not independently verify scientific assertions or source authenticity.'])
        if m['url']: source['url']=m['url']
        if m['studyDate']: source['date']=m['studyDate']
        source_entries = [source] if m['source'] or m['url'] else []
        retrieved_sources = r.get('processing', {}).get('sources')
        if retrieved_sources:
            source_entries = [{'id': item['evidenceId'], 'title': item.get('title') or urlsplit(item['url']).hostname or 'Submitted source',
                               'url': item['url'], 'status': 'unverified',
                               'checked': 'Content ' + item['status'].replace('_', ' ') + '. ' + item.get('reason', '') + ' Authenticity remains unverified.',
                               'limitations': ['Source reading and scientific verification have separate states.']} for item in retrieved_sources]
        calculations = [comparison for table in r.get('processing', {}).get('datasets', []) for comparison in table['comparisons']]
        checks = [{'id': c['id'], 'kind': 'calculation', 'text': c['indicator'] + ' · ' + c['year'] + '. ' + c['method'],
                   'value': c['difference'], 'unit': c['differenceUnit'], 'citations': [c['id']], 'sourceVerified': False} for c in calculations]
        payload = {'sources':source_entries,'files':[{**{k:v for k,v in f.items() if k!='sha256'}, 'url':f'/api/analyses/{analysis_id}/files/{f["id"]}'} for f in r['files']],
                   'study':r['packet']['study'],'checks':checks,'uncertainty':[m['uncertainty']] if m['uncertainty'] else ['Uncertainty information unavailable.'],
                   'contract':{'inputFacts':r['packet'],'computedFacts':r.get('processing', {}),'sourceProvenance':'unverified','constraints':r['packet']['limitations'],'fileHashes':{f['id']:f['sha256'] for f in r['files']},
                               'agentInputs':r.get('agentInputs', {}),'promptSnapshots':r.get('promptSnapshots', {}),
                               'failedOutputs':r.get('failedOutputs', {})},
                   'permissions':{'contractDownload':True,'dataDownload':False}}
        if r['dataset']: payload['dataset']={**r['dataset'],'serverPaginated':True,'totalRows':len(r['dataset']['rows']),'page':1,'pageSize':25,'rows':r['dataset']['rows'][:25]}
        return self.response(SectionResponse,payload)

    def get_analysis_dataset(self,analysis_id):
        return self.dataset_response(self.record(analysis_id))

    def dataset_response(self, r):
        if r['dataset'] is None: raise NotFound()
        q = self.query(DatasetQuery,{'page':'1','pageSize':'25','search':'','sort':'-1','direction':'asc'})
        ds = r['dataset']; rows = ds['rows']
        if q['search']: rows = [row for row in rows if any(q['search'].casefold() in str(v).casefold() for v in row)]
        if q['sort']>=len(ds['columns']): raise UnprocessableEntity()
        if q['sort']>=0: rows = sorted(rows,key=lambda row:str(row[q['sort']]).casefold(),reverse=q['direction']=='desc')
        start=(q['page']-1)*25
        return self.response(Dataset,{**ds,'rows':rows[start:start+25],'totalRows':len(rows),'serverPaginated':True,'page':q['page'],'pageSize':25})

    def get_analysis_visualizations(self,analysis_id):
        r = self.record(analysis_id)
        vis = {'changes':[],'provenance':'Original user upload; no neutralization performed.','generationStatus':'unavailable',
               'unavailableReason':'No scientifically specified neutral-chart generator is configured.','warnings':LIMITATIONS}
        original = next((f for f in r['files'] if f['mediaType'].startswith('image/')),None)
        if original:
            vis['original']=f'/api/analyses/{analysis_id}/files/{original["id"]}'
            vis['originalDescription']='Original user-supplied chart; not a verified rendering.'
        return self.response(SectionResponse,{'visualizations':vis,'permissions':{'assetDownload':True}})

    def get_analysis_council(self,analysis_id):
        r=self.record(analysis_id)
        return self.response(SectionResponse,{'reviews':r['reviews'],'disagreements':r['disagreements']})

    def list_analysis_audit(self,analysis_id):
        return self.response(SectionResponse,{'events':self.record(analysis_id)['events'],'permissions':{'auditDownload':True}})

    def get_analysis_report(self,analysis_id):
        r=self.record(analysis_id)
        if r['report'] is None: raise NotFound()
        return self.response(SectionResponse,r['report'])

    def list_reports(self):
        records=[]
        for r in self.records():
            if r['report'] is None: continue
            a=r['analysis']
            records.append({'id':r['id'],'analysisId':r['id'],'title':a['title'],'createdAt':r['report']['report']['generatedAt'],
                            'status':a.get('assessment','not_evaluated'),'mode':a['mode'],'summary':'Exploratory AI review; not scientifically verified.',
                            'permissions':{'delete':not bool(r.get('researchCaseId')),'json':True}})
        return self.response(ReportList,self.page(records,self.query(ReportListQuery)))

    def get_report(self,report_id):
        return self.get_analysis_report(report_id)

    def delete_report(self,report_id):
        with self.store.lock:
            r=self.record(report_id)
            if r.get('researchCaseId'): raise Conflict()
            if r['report'] is None: raise NotFound()
            r['report']=None
            self.store.event(r,'reports','report_deleted')
            self.store.put('analysis',r)
        return '',204

    def compare_analyses(self):
        q=self.query(ComparisonQuery)
        a,b=self.record(q['analysisA']),self.record(q['analysisB'])
        dimensions=[]
        for key,label,va,vb in [('claim','Claim',a['analysis']['claim'],b['analysis']['claim']),('mode','Mode',a['analysis']['mode'],b['analysis']['mode']),
                                ('study','Study design',a['metadata']['studyDesign'],b['metadata']['studyDesign']),('population','Population',a['metadata']['population'],b['metadata']['population']),
                                ('source','Source status',a['analysis']['sourceStatus'],b['analysis']['sourceStatus'])]:
            dimensions.append({'key':key,'label':label,'a':va or None,'b':vb or None,'relation':'same' if va and va==vb else 'different' if va and vb else 'unknown'})
        return self.response(ComparisonResponse,{'analysisA':q['analysisA'],'analysisB':q['analysisB'],'comparability':'unknown',
                  'reasons':['Metadata differences are descriptive. Scientific comparability has not been evaluated; no winner or accuracy score is calculated.'],'dimensions':dimensions})

    def list_activity(self):
        q=self.query(ActivityQuery,{'limit':'10'})
        events=[{'id':e['id'],'timestamp':e['timestamp'],'description':e['type'].replace('_',' '),'analysisId':r['id']} for r in self.records() for e in r['events']]
        events.sort(key=lambda e:e['timestamp'],reverse=True)
        return self.response(ActivityResponse,{'items':events[:q['limit']]})

    def list_integrations(self):
        operator()
        return self.response(IntegrationList,{'items':[
            {'id':'api','name':'Direct workspace API','category':'api','status':'available','overview':'Local Flask workspace API.',
             'capabilities':['Persisted exploratory analyses','Actual review execution and audit records'],'requirements':['Running Flask application'],'instructions':['Use the documented same-origin /api development proxy.'],'documentation':'api','endpoint':'/api','canTest':True},
            {'id':'provider','name':'Review provider','category':'developer','status':'configured' if self.provider.configured else 'not_configured',
             'overview':'Selected server-side AI provider. Configured does not establish account access or model availability.',
             'capabilities':['Structured exploratory AI review'],'requirements':['Configured model ID and appropriate server-side credentials'],
             'instructions':['Set EVIDENCETWIN_PROVIDER and its server environment variables.'],'documentation':'api','canTest':bool(self.provider.configured and isinstance(self.provider, OllamaProvider))},
            *[{'id':key,'name':name,'category':key,'status':'planned','overview':'This integration is not implemented.',
                'capabilities':[],'requirements':['Owner implementation'],'instructions':['Read the integration requirements.'],
                'documentation':doc,'canTest':False} for key,name,doc in [('mcp','MCP Server','mcp'),('skill','AI Assistant Skills','skills')]]]})

    def test_integration(self,integration_id):
        operator()
        if integration_id not in ('api','provider'): return not_implemented('This integration is not implemented.')
        if integration_id=='provider' and not isinstance(self.provider,OllamaProvider):
            return not_implemented('A non-billable provider connection probe is not implemented for this adapter.')
        ok = integration_id=='api' or (self.provider.configured and self.provider.probe())
        return jsonify({'status':'reachable' if ok else 'failed','message':'API reachable.' if integration_id=='api' else 'Configured model discovered.' if ok else 'Provider/model access could not be confirmed.','checkedAt':now()})

    def list_research_cases(self):
        return jsonify({'items':CASES})

    def get_research_case(self,case_id):
        case=next((c for c in CASES if c['id']==case_id),None)
        if case is None: raise NotFound()
        return jsonify(case)

    def list_benchmarks(self):
        return self.response(BenchmarkList,self.page(self.records('benchmark'),self.query(BenchmarkListQuery),title='name'))

    def get_benchmark(self,benchmark_id):
        return self.response(BenchmarkResponse,owned(self.store,'benchmark',benchmark_id))

    def create_benchmark(self):
        return not_implemented('Benchmark execution requires a specified scoring rubric, ground truth and an evaluator. No run was created.')

    def capabilities(self):
        ready=bool(self.provider.configured)
        return self.response(CapabilitiesResponse,{'providers':[{'name':getattr(self.provider,'name','Ollama'),'status':'configured' if ready else 'not_configured'}],
            'jobAvailability':'available' if ready else 'unavailable','activity':True,
            'analyses':{'create':ready,'delete':True,'retry':ready,'maxClaims':10,'modes':['exploratory'],'reviewDepths':['focused','council']},
            'services':[{'name':name,'status':status} for name,status in [('Exploratory AI review','available' if ready else 'not_configured'),('Scientific Core','unavailable'),('Source verification','unavailable'),('Neutral visualization','unavailable'),('Reports','available'),('Benchmarks','unavailable'),('MCP','unavailable')]],
            'research':{'comparison':True,'benchmarks':{'read':True,'create':False},'reports':{'read':True},'integrations':{'read':True}}})


def install_runtime(app):
    runtime=Runtime(app)
    app.extensions['evidencetwin']=runtime
    install_access(app, runtime.store)
    from .research_cases import install_research_cases
    install_research_cases(app, runtime)
    install_report_translations(app, runtime)
    # Keep the original Blueprint ownership and function names. Existing skeleton
    # mode remains available for contract-only deployments and structural tests.
    for endpoint, original in list(app.view_functions.items()):
        name=endpoint.split('.')[-1]
        if endpoint=='system.health' or not hasattr(runtime,name): continue
        handler=getattr(runtime,name)
        def make_view(handler,original):
            @wraps(original)
            def view(**params):
                try:
                    return handler(**params)
                except (ValidationError, json.JSONDecodeError, UnicodeError, csv.Error, Image.DecompressionBombError, Image.DecompressionBombWarning):
                    raise UnprocessableEntity() from None
                except (Image.UnidentifiedImageError,):
                    raise UnprocessableEntity() from None
            return view
        app.view_functions[endpoint]=make_view(handler,original)

    for path, method, handler in [('/api/settings/ai','GET',runtime.get_ai_settings),('/api/settings/ai','POST',runtime.save_ai_settings),('/api/settings/ai/test','POST',runtime.test_ai_settings)]:
        def make_settings_view(handler):
            def view():
                try:
                    return handler()
                except (ValidationError, json.JSONDecodeError, ValueError):
                    raise UnprocessableEntity() from None
            return view
        app.add_url_rule(path,endpoint='integrations.'+handler.__name__,view_func=make_settings_view(handler),methods=[method])

    def file_asset(analysis_id,file_id):
        record=runtime.record(analysis_id)
        file=next((f for f in record['files'] if f['id']==file_id),None)
        if file is None: raise NotFound()
        return send_file(runtime.store.uploads/analysis_id/file_id,mimetype=file['mediaType'],
                         as_attachment=not file['mediaType'].startswith('image/'),download_name=file['name'])
    app.add_url_rule('/api/analyses/<analysis_id>/files/<file_id>',endpoint='evidence.file_asset',view_func=file_asset,methods=['GET'])
