"""Application tests use explicit deterministic provider doubles, never fake production science."""
from io import BytesIO
import json
import threading
from time import monotonic, sleep
import pytest
from PIL import Image
from evidencetwin_backend import create_app
from evidencetwin_backend.services.provider import ROLES, ProviderFailure
from evidencetwin_backend.contracts.common import validate_contract
from evidencetwin_backend.contracts.analyses import Analysis
from evidencetwin_backend.contracts.inspection import SectionResponse, Dataset

class TestProvider:
    __test__=False
    configured=True
    name='Test transport only'
    model='test-model'
    def __init__(self):
        self.calls=[]; self.fail=set(); self.bad_ref=False
        self.started=threading.Event(); self.block=None
    def probe(self): return True
    def chat(self,role,packet,images,schema):
        self.calls.append((role,packet,images));self.started.set()
        if self.block: assert self.block.wait(5)
        if role in self.fail: raise ProviderFailure('TEST ONLY PRIVATE ERROR')
        evidence=packet['evidence'][0]['id']
        if role in ROLES:
            data={'agent_id':role,'review_status':'completed','overall_assessment':'Synthetic test interpretation.',
                  'claim_assessments':[{'claim_id':c['id'],'position':'cannot_assess','rationale':'Test fixture only.','evidence_refs':[]} for c in packet['claims']],
                  'findings':[{'finding_id':ROLES[role][3]+'1','severity':'informational','category':'test','title':'Test only','observation':'Synthetic test observation.',
                               'why_it_matters':'Test fixture only.','evidence_refs':['invalid-id'] if self.bad_ref else [evidence],'recommendation':'Test only.'}],
                  'limitations':['Synthetic provider in tests.'],'missing_information':[]}
        elif role=='cross_reviewer':
            data={'review_status':'completed','critiques':[],'unresolved_disagreements':[],
                  'overall_quality_assessment':'Synthetic cross-review.','limitations':['Test only.']}
        else:
            data={'case_id':packet['case_id'],'overall_verdict':'supported','claim_results':[{'claim_id':c['id'],'verdict':'supported','explanation':'Synthetic test verdict.',
                  'supporting_evidence_refs':[evidence],'contradicting_evidence_refs':[],'reviewer_finding_refs':[],'unresolved_issues':[]} for c in packet['claims']],
                  'key_findings':['Synthetic judge result.'],'agent_disagreements':[],'limitations':['Test only.'],'recommended_wording':'Test only.'}
        return {'data':data,'model':'test-model','usage':{'prompt_eval_count':10}}

@pytest.fixture
def runtime(tmp_path, monkeypatch):
    # Source transport has its own boundary tests. Existing workflow fixtures
    # must not depend on a public website or dispatch real research requests.
    monkeypatch.setattr('evidencetwin_backend.science.processing.retrieve_source', lambda url, directory: {
        'url': url, 'status': 'unavailable', 'reason': 'External retrieval disabled in isolated test fixtures.',
        'authenticity': 'unverified', 'contentVerification': 'not_performed'})
    provider=TestProvider()
    app=create_app({'TESTING':True,'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(tmp_path),'REVIEW_PROVIDER':provider,'WORKERS':2,'QUEUE_LIMIT':4})
    yield app,app.test_client(),provider
    if provider.block: provider.block.set()
    app.extensions['evidencetwin'].workflow.shutdown()


def metadata(**updates):
    return {'source':'Test study','url':'https://example.org/study','studyDate':'','studyDesign':'Unknown','population':'','uncertainty':'',
            'context':'','claims':['Test this claim.'],'claim':'Test this claim.','mode':'exploratory','reviewDepth':'focused',**updates}


def upload(client,meta=None,files=None):
    data={'metadata':json.dumps(meta or metadata())}
    data['files']=files if files is not None else [(BytesIO(b'label,value\na,42\nb,40\n'),'data.csv')]
    return client.post('/api/analyses',data=data,content_type='multipart/form-data')


def wait(app,record_id):
    end=monotonic()+5
    while monotonic()<end:
        record=app.extensions['evidencetwin'].store.get('analysis',record_id)
        if record['analysis']['status'] not in ('queued','running'): return record
        sleep(.01)
    pytest.fail('Local job did not finish')


def create(app,client,**updates):
    r=upload(client,metadata(**updates)); assert r.status_code==202,r.json
    return wait(app,r.json['id'])


def test_full_council_pipeline_and_contracts(runtime):
    app,c,p=runtime
    r=create(app,c,reviewDepth='council')
    a=c.get('/api/analyses/'+r['id']).json
    validate_contract(Analysis,a)
    assert a['status']=='completed_with_limitations'
    assert a['assessment']=='not_evaluated' # Synthetic judge "supported" must not become a verified badge.
    assert all(f['kind']=='interpretation' and f['sourceVerified'] is False for f in a['findings'])
    assert [role for role,_,_ in p.calls]==[*ROLES,'cross_reviewer','evidence_judge']
    for _,packet,_ in p.calls[:4]: assert 'reviewer_reports' not in packet
    assert len(p.calls[4][1]['reviewer_reports'])==4
    assert 'cross_review' in p.calls[5][1]
    for section in ('evidence','visualizations','council','audit','report'):
        response=c.get(f'/api/analyses/{r["id"]}/{section}')
        assert response.status_code==200,response.json
        validate_contract(SectionResponse,response.json)
    council=c.get(f'/api/analyses/{r["id"]}/council').json
    assert all(v['independentExecution'] for v in council['reviews'][:4])
    assert council['reviews'][-1]['report']['output']['overall_verdict']=='supported'
    evidence=c.get(f'/api/analyses/{r["id"]}/evidence').json
    assert evidence['sources'][0]['status']=='unverified'
    assert evidence['checks']==[]
    assert evidence['contract']['inputFacts']['scientific_pipeline']['source_verification']=='unavailable'
    assert c.get('/api/reports').json['total']==1
    assert c.get('/api/activity').json['items']


def test_focused_review_does_not_fabricate_council(runtime):
    app,c,p=runtime;r=create(app,c)
    assert [x[0] for x in p.calls]==['visual_analyst']
    assert len(r['reviews'])==1 and 'evidence_judge' not in r['raw']

@pytest.mark.parametrize('failure',['visual_analyst','cross_reviewer','evidence_judge'])
def test_partial_reviewer_failures(runtime,failure):
    app,c,p=runtime;p.fail.add(failure)
    r=create(app,c,reviewDepth='council')
    assert r['analysis']['status']=='completed_with_limitations'
    assert any(v['status']=='failed' for v in r['reviews'])
    if failure=='visual_analyst': assert len(p.calls)==4
    if failure=='cross_reviewer': assert len(p.calls)==5
    assert r['analysis']['assessment']=='not_evaluated'


def test_invalid_references_fail_without_leaking_provider_error(runtime):
    app,c,p=runtime;p.bad_ref=True
    r=create(app,c)
    assert r['analysis']['status']=='failed'
    assert r['report'] is None
    assert 'PRIVATE' not in json.dumps(r)
    assert c.get('/api/reports').json['items']==[]


def test_failure_retry_then_success(runtime):
    app,c,p=runtime;p.fail={'visual_analyst'}
    r=create(app,c); assert r['analysis']['status']=='failed'
    p.fail.clear()
    assert c.post(f'/api/analyses/{r["id"]}/retry').status_code==202
    r=wait(app,r['id']);assert r['analysis']['status']=='completed_with_limitations'
    assert c.post(f'/api/analyses/{r["id"]}/retry').status_code==409
    assert len(r['reviews'])==1


def test_cancel_and_discard_inflight_output(runtime):
    app,c,p=runtime;p.block=threading.Event()
    response=upload(c);record_id=response.json['id'];assert p.started.wait(2)
    assert c.post(f'/api/analyses/{record_id}/cancel').status_code==202
    p.block.set()
    app.extensions['evidencetwin'].workflow.pool.submit(lambda:None).result(2)
    r=wait(app,record_id)
    assert r['analysis']['status']=='cancelled' and r['report'] is None
    assert c.delete(f'/api/analyses/{record_id}').status_code==204


def test_delete_running_is_conflict_and_queue_capacity(runtime):
    app,c,p=runtime;p.block=threading.Event()
    ids=[upload(c).json['id'] for _ in range(4)]
    assert upload(c).status_code==503
    assert len(list(app.extensions['evidencetwin'].store.uploads.iterdir()))==4
    assert c.delete('/api/analyses/'+ids[0]).status_code==409
    p.block.set()


def test_search_sort_filters_report_deletion_and_comparison(runtime):
    app,c,_=runtime
    a=create(app,c,source='Alpha',population='Group A')
    b=create(app,c,source='Beta',population='Group B')
    assert c.get('/api/analyses?search=Alpha').json['total']==1
    assert c.get('/api/analyses?search=missing').json['total']==0
    assert c.get('/api/analyses?sort=title:asc&pageSize=1').json['items'][0]['title']=='Alpha'
    assert c.get('/api/analyses?mode=verified').json['total']==0
    assert c.get('/api/reports?status=supported').json['total']==0
    assert c.get('/api/reports?from=2099-01-01').json['total']==0
    report_id=a['id']
    assert c.get('/api/reports/'+report_id).status_code==200
    assert c.delete('/api/reports/'+report_id).status_code==204
    assert c.get('/api/reports/'+report_id).status_code==404
    comp=c.get('/api/comparisons',query_string={'analysisA':a['id'],'analysisB':b['id']})
    assert comp.status_code==200 and comp.json['comparability']=='unknown'
    assert comp.json['analysisA']==a['id'] and comp.json['analysisB']==b['id']
    assert c.delete('/api/analyses/'+a['id']).status_code==204
    assert c.get('/api/analyses/'+a['id']).status_code==404


def test_dataset_pagination_and_provenance(runtime):
    app,c,_=runtime
    response=upload(c,files=[(BytesIO(('label,value\n'+''.join(f'row{i},{i}\n' for i in range(60))).encode()),'data.csv')])
    r=wait(app,response.json['id']);base='/api/analyses/'+r['id']
    page=c.get(base+'/dataset?page=2&pageSize=25&sort=0&direction=asc&search=').json
    validate_contract(Dataset,page)
    assert page['totalRows']==60 and len(page['rows'])==25
    evidence=c.get(base+'/evidence').json
    assert len(evidence['dataset']['rows'])==25 and evidence['dataset']['serverPaginated']
    assert c.get(base+'/dataset?sort=99').status_code==422
    assert c.get(base+'/dataset?sort=0&sort=1').status_code==422

@pytest.mark.parametrize('updates',[{'mode':'verified'},{'claim':'Different claim.'},{'claims':['Test this claim.','Test this claim.']},{'url':'http://user:secret@example.com'},{'url':'file:///etc/passwd'}])
def test_invalid_analysis_metadata(runtime,updates):
    _,c,_=runtime;assert upload(c,metadata(**updates)).status_code==422

@pytest.mark.parametrize('data,name,status',[(b'x','chart.exe',415),(b'not png','chart.png',422),(b'x','paper.pdf',422),(b'a,b\n1\n','data.csv',422),(b'a,a\n1,2\n','data.csv',422),(b'\xff','data.csv',422),(b'','data.csv',422)])
def test_upload_validation(runtime,data,name,status):
    app,c,_=runtime
    assert upload(c,files=[(BytesIO(data),name)]).status_code==status
    assert not list(app.extensions['evidencetwin'].store.uploads.iterdir())
    assert c.get('/api/analyses').json['total']==0


def test_duplicate_upload_and_image_asset(runtime):
    app,c,_=runtime
    assert upload(c,files=[(BytesIO(b'a\n1'),'a.csv'),(BytesIO(b'a\n1'),'b.csv')]).status_code==422
    image=BytesIO();Image.new('RGB',(20,10),'white').save(image,format='PNG');image.seek(0)
    response=upload(c,files=[(image,'chart.png')]);r=wait(app,response.json['id'])
    assert len(r['files'])==1
    url=c.get(f'/api/analyses/{r["id"]}/visualizations').json['visualizations']['original']
    asset=c.get(url);assert asset.status_code==200 and asset.mimetype=='image/png'
    assert c.get(url+'/../missing').status_code==404
    assert c.get(f'/api/analyses/{r["id"]}/files/missing').status_code==404
    assert app.extensions['evidencetwin'].provider.calls[0][2]


def test_no_provider_unavailable_capability_and_defined_gaps(runtime):
    _,c,p=runtime;p.configured=False
    caps=c.get('/api/capabilities').json
    assert caps['analyses']['create'] is False and caps['analyses']['modes']==['exploratory']
    assert caps['research']['benchmarks']=={'read':True,'create':False}
    assert upload(c).status_code==503
    assert c.post('/api/benchmarks',json={}).status_code==501
    assert c.get('/api/benchmarks').json['total']==0
    assert c.get('/api/cases').json['items'][0]['sample'] is True
    assert c.get('/api/cases/a3').json['rows']==[['Grade 9',40.3],['Grade 10',39.7]]
    assert c.get('/api/cases/no-such').status_code==404
    assert c.post('/api/integrations/mcp/test').status_code==501


def test_persistence_restart_and_interrupted_job_recovery(tmp_path):
    provider=TestProvider()
    config={'TESTING':True,'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(tmp_path),'REVIEW_PROVIDER':provider}
    app=create_app(config);c=app.test_client();r=create(app,c)
    store=app.extensions['evidencetwin'].store
    r['analysis']['status']='running';store.put('analysis',r)
    app.extensions['evidencetwin'].workflow.shutdown()
    second=create_app(config)
    state=second.test_client().get('/api/analyses/'+r['id']).json
    assert state['status']=='failed' and state['actions']['retry']
    assert len(provider.calls)==1 # no silent replay
    second.extensions['evidencetwin'].workflow.shutdown()


def test_duplicate_worker_process_fails_closed(runtime):
    app,_,_=runtime
    with pytest.raises(RuntimeError,match='active backend process'):
        create_app({'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(app.extensions['evidencetwin'].store.root)})


def test_mutations_reject_cross_origin_browser_requests(runtime):
    _,c,_=runtime
    assert c.post('/api/analyses',headers={'Origin':'https://untrusted.example'}).status_code==403
    assert c.post('/api/analyses',headers={'Origin':'http://localhost'}).status_code==415


def test_actual_frontend_parsers_accept_runtime_outputs(runtime):
    from pathlib import Path
    import subprocess
    import shutil
    from werkzeug.serving import make_server
    app,c,_=runtime
    r=create(app,c,reviewDepth='council');record_id=r['id']
    frontend=Path(__file__).resolve().parents[2]/'frontend'
    if not shutil.which('node') or not (frontend/'node_modules/vite').exists(): pytest.skip('Requires existing frontend Node dependencies')
    script=r'''
import assert from 'node:assert/strict';
process.env.VITE_API_BASE_URL=process.argv[1];process.env.VITE_ANALYSIS_FIXTURES='false';
const {createServer}=await import('vite');
const server=await createServer({server:{middlewareMode:true},appType:'custom'});
try {
 const w=await server.ssrLoadModule('/src/workspace-api.ts');
 const i=await server.ssrLoadModule('/src/research-api.ts');
 const r=await server.ssrLoadModule('/src/features/research/api.ts');
 const id=process.argv[2],signal=new AbortController().signal;
 const caps=await w.getCapabilities(signal);assert.equal(caps.analyses.create,true);
 const opts={search:'',status:'',mode:'',verdict:'',sort:'createdAt:desc',page:1};
 assert.equal((await w.getAnalyses(opts,signal)).total,1);
 assert.equal((await i.readAnalysis(id,signal)).id,id);
 for(const section of ['evidence','visualizations','council','audit','report'])await i.readAnalysisSection(id,section,signal);
 assert.equal((await r.readReports({search:'',status:'',mode:'',sort:'createdAt:desc',page:1},signal)).total,1);
 await r.readReport(id,signal);await r.readIntegrations(signal);await r.readComparison(id,id,signal);
 assert.equal((await w.getActivity(signal)).items.length>0,true);
 console.log('Runtime adapter contracts passed');
} finally{await server.close()}
'''
    server=make_server('127.0.0.1',0,app);worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    try:
        result=subprocess.run(['node','--input-type=module','-e',script,f'http://127.0.0.1:{server.server_port}/api',record_id],cwd=frontend,capture_output=True,text=True,timeout=45)
        assert result.returncode==0,result.stderr
        assert 'Runtime adapter contracts passed' in result.stdout
    finally:
        server.shutdown();worker.join(5);server.server_close()


def test_json_dataset_matches_frontend_upload_contract(runtime):
    app,c,_=runtime
    payload={'columns':['group','value'],'rows':[['a',42],['b',40]]}
    response=upload(c,files=[(BytesIO(json.dumps(payload).encode()),'data.json')])
    assert response.status_code==202,response.json
    record=wait(app,response.json['id'])
    assert record['dataset']==payload
    assert upload(c,files=[(BytesIO(b'{"columns": ["a"], "rows": [[1,2]]}'),'bad.json')]).status_code==422


def test_authentication_hook_applies_to_runtime_assets_and_records(tmp_path):
    from werkzeug.exceptions import Unauthorized
    def auth(): raise Unauthorized()
    app=create_app({'TESTING':True,'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(tmp_path),'AUTHENTICATE_REQUEST':auth})
    c=app.test_client()
    assert c.get('/api/health').status_code==200
    assert c.get('/api/analyses').status_code==401
    assert c.get('/api/analyses/anything/files/anything').status_code==401
    assert c.options('/api/analyses').status_code==200
    app.extensions['evidencetwin'].workflow.shutdown()


def test_selected_educational_case_is_explicit_in_model_input(runtime):
    app,c,p=runtime
    r=upload(c,metadata(caseId='a1'),files=[])
    assert r.status_code==202
    record=wait(app,r.json['id'])
    packet=p.calls[0][1]
    assert packet['educational_case']=='a1'
    assert 'Illustrative' in packet['dataset']['notes'][0]
    assert any('educational' in limitation for limitation in record['analysis']['limitations'])


def test_complete_dataset_queries_feed_roles_and_report(runtime, monkeypatch):
    app, client, provider = runtime
    original_chat = provider.chat
    def request_rows(role, packet, images, schema):
        reply = original_chat(role, packet, images, schema)
        if role == 'visual_analyst' and not packet.get('requested_query_results'):
            reply['data']['requested_queries'] = [{'filters': {'Entity': 'Group Beta', 'Year': '2024'}, 'limit': 1}]
        return reply
    monkeypatch.setattr(provider, 'chat', request_rows)
    claim = 'Group Alpha was higher than Group Beta in 2024.'
    rows = 'Entity,Code,Year,Reported rate (%)\n' + ''.join(f'Other {i},X,2024,1\n' for i in range(430)) + 'Group Alpha,A,2024,22.4\nGroup Beta,B,2024,13.7\n'
    accepted = upload(client, metadata(url='', claim=claim, claims=[claim], reviewDepth='council'), [(BytesIO(rows.encode()), 'data.csv')])
    record = wait(app, accepted.json['id'])
    assert record['analysis']['status'] == 'completed_with_limitations'
    assert record['analysis']['assessment'] == 'not_evaluated'
    assert record['processing']['datasets'][0]['comparisons'][0]['difference'] == '8.7'
    assert record['agentInputs']['visual_analyst']['requested_query_results'][0]['records'][0]['rowNumber'] == 433
    assert any('8.7 percentage points' in section['body'] for section in record['report']['sections'])
    assert record['promptSnapshots']['evidence-access-v2.md']
    packet = provider.calls[0][1]
    assert any(row[0] == 'Group Beta' for row in packet['dataset']['rows'])
    assert 'reviewer_reports' not in packet
    assert client.get(f"/api/analyses/{record['id']}/processing").status_code == 200
