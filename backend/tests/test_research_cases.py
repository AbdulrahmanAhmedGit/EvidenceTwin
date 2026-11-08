"""Narrow integrity checks; temporary data and explicit synthetic provider only."""
from io import BytesIO
import json
from uuid import uuid4
import pytest
from werkzeug.security import generate_password_hash
from evidencetwin_backend import create_app
from test_runtime import TestProvider, metadata, wait

@pytest.fixture
def pilot(tmp_path):
    provider = TestProvider()
    app = create_app({'TESTING': True, 'RUNTIME_ENABLED': True, 'ACCOUNTS_ENABLED': True,
                      'DATA_DIRECTORY': str(tmp_path), 'REVIEW_PROVIDER': provider})
    store = app.extensions['evidencetwin'].store
    for name, role in [('first','researcher'),('second','researcher'),('operator','operator')]:
        store.put('account', {'id':name,'name':name,'role':role,'active':True,'version':1,
                              'passwordHash':generate_password_hash('test-password-only')})
    yield app, provider
    app.extensions['evidencetwin'].workflow.shutdown()

def login(app, name):
    c = app.test_client()
    assert c.post('/api/session/login', json={'name':name,'password':'test-password-only'}).status_code == 200
    return c

def save(c, meta=None, files=None, case=None):
    body = {'metadata':json.dumps(meta or metadata())}
    if files is not None: body['files'] = files
    if case: body['retainedFiles'] = json.dumps([f['id'] for f in case['files']])
    return c.post('/api/research-cases'+('/'+case['id']+'/revisions' if case else ''), data=body, content_type='multipart/form-data',
                  headers={'If-Match':case['currentRevision']} if case else {})

def test_question_save_and_immutable_revision_without_provider(pilot):
    app, provider = pilot
    provider.configured = False
    c = login(app, 'first')
    first = save(c).get_json()
    assert first['files'] == [] and first['analyses'] == []
    response = save(c, metadata(claim='Revised question.', claims=['Revised question.']),
                    [(BytesIO(b'item,value\na,1\n'), 'بيانات.csv')], first)
    assert response.status_code == 201
    second = response.json
    assert second['id'] == first['id'] and second['revisionCount'] == 2
    old = c.get(f"/api/research-cases/{first['id']}/revisions/{first['currentRevision']}").json
    assert old['metadata']['claim'] == metadata()['claim'] and old['files'] == []
    assert c.post(f"/api/research-cases/{first['id']}/revisions", data={'metadata':json.dumps(metadata())},
                  headers={'If-Match':first['currentRevision']}).status_code == 409
    file = second['files'][0]
    assert file['name'] == 'بيانات.csv'
    assert c.get(f"/api/research-cases/{first['id']}/revisions/{second['currentRevision']}/dataset").json['rows'] == [['a','1']]
    content = c.get(f"/api/research-cases/{first['id']}/revisions/{second['currentRevision']}/files/{file['id']}")
    assert content.data == b'item,value\na,1\n' and 'attachment' in content.headers['Content-Disposition']
    assert len(file['sha256']) == 64 and provider.calls == []

def test_ownership_idempotent_runs_and_operator_boundary(pilot):
    app, provider = pilot
    a, b = login(app, 'first'), login(app, 'second')
    case = save(a, files=[(BytesIO(b'item,value\na,1\n'),'data.csv')]).json
    assert b.get('/api/research-cases').json['total'] == 0
    assert b.get('/api/research-cases/'+case['id']).status_code == 404
    request = {'revisionId':case['currentRevision'],'requestId':str(uuid4()),'consent':True}
    assert b.post('/api/research-cases/'+case['id']+'/analyses',json=request).status_code == 404
    response = a.post('/api/research-cases/'+case['id']+'/analyses', json=request)
    assert response.status_code == 202
    run_id = response.json['id'];wait(app, run_id)
    assert a.post('/api/research-cases/'+case['id']+'/analyses', json=request).json['id'] == run_id
    assert len(app.extensions['evidencetwin'].store.all('analysis')) == 1
    file = case['files'][0]['id']
    for route in [f'/analyses/{run_id}',f'/analyses/{run_id}/evidence',f'/analyses/{run_id}/council',
                  f'/analyses/{run_id}/audit',f'/analyses/{run_id}/report',f'/reports/{run_id}',
                  f'/analyses/{run_id}/processing',f'/analyses/{run_id}/report-translations',f'/analyses/{run_id}/report-translations/other-job',f'/analyses/{run_id}/source-snapshot',f'/analyses/{run_id}/dataset-query',
                  f'/research-cases/{case["id"]}/revisions/{case["currentRevision"]}/processing',
                  f'/analyses/{run_id}/files/{file}',f'/research-cases/{case["id"]}/revisions/{case["currentRevision"]}/files/{file}',
                  f'/research-cases/{case["id"]}/revisions/{case["currentRevision"]}/dataset']:
        assert b.get('/api'+route).status_code == 404, route
    assert b.post(f'/api/analyses/{run_id}/report-translations',json={'targetLanguage':'ar'}).status_code == 404
    assert b.get('/api/analyses').json['total'] == 0
    assert b.get('/api/reports').json['total'] == 0
    assert b.get('/api/activity').json['items'] == []
    for action in ['cancel','retry']:
        assert b.post('/api/analyses/'+run_id+'/'+action).status_code == 404
    assert a.delete('/api/analyses/'+run_id).status_code == 409
    assert a.get('/api/settings/ai').status_code == 403
    assert login(app,'operator').get('/api/settings/ai').status_code == 200

def test_invalid_consent_upload_and_stale_revision(pilot):
    app, _ = pilot;c = login(app,'first');case = save(c).json
    assert c.post('/api/research-cases/'+case['id']+'/analyses', json={'revisionId':case['currentRevision'],'requestId':str(uuid4()),'consent':False}).status_code == 422
    assert save(c, files=[(BytesIO(b'bad'),'data.xlsx')]).status_code == 415
    assert c.get('/api/research-cases').json['total'] == 1
    assert len(list(app.extensions['evidencetwin'].store.uploads.iterdir())) == 1

def test_sessions_revocation_origin_and_legacy_protection(pilot):
    app, _ = pilot;c = login(app,'first')
    assert app.test_client().get('/api/research-cases').status_code == 401
    assert c.post('/api/session/logout', headers={'Origin':'https://untrusted.invalid'}).status_code == 403
    store = app.extensions['evidencetwin'].store
    # Complete legacy-shaped record, retained without silent ownership assignment.
    store.put('analysis', {'id':'legacy','metadata':metadata(),'files':[], 'packet':{},'analysis':{
        'id':'legacy','title':'Legacy input','status':'draft','mode':'exploratory','createdAt':'2026-11-01T00:00:00Z',
        'claim':'Legacy input','limitations':[],'findings':[]}})
    assert c.get('/api/analyses/legacy').status_code == 404
    assert login(app,'operator').get('/api/analyses/legacy').status_code == 200
    account = store.get('account','first');account['active'] = False;store.put('account',account)
    assert c.get('/api/research-cases').status_code == 401

def test_account_cli_can_operate_beside_running_workspace(pilot):
    import click
    from click.testing import CliRunner
    from evidencetwin_backend.services.access import register_account_commands
    app, _ = pilot
    group = click.Group()
    register_account_commands(group, app.extensions['evidencetwin'].store)
    runner = CliRunner()
    response = runner.invoke(group, ['invite-researcher','--name','invited'], input='test-password-only\ntest-password-only\n')
    assert response.exit_code == 0, response.output
    assert 'test-password-only' not in response.output
    user = login(app, 'invited')
    response = runner.invoke(group, ['disable-researcher','--name','invited'])
    assert response.exit_code == 0
    assert user.get('/api/research-cases').status_code == 401
