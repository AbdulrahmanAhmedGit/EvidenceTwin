"""Configuration uses temporary private server storage; no live credentials."""
import json
import stat
import threading
import pytest
from evidencetwin_backend import create_app
from test_runtime import TestProvider, metadata, upload, wait
from evidencetwin_backend.services.transports import make_provider

@pytest.fixture
def settings_app(tmp_path):
    app=create_app({'TESTING':True,'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(tmp_path)})
    yield app,app.test_client()
    app.extensions['evidencetwin'].workflow.shutdown()

def test_save_keep_replace_remove_and_never_return_key(settings_app):
    app,c=settings_app
    assert c.get('/api/settings/ai').status_code==200
    payload={'provider':'openai','model':'test-vision','apiKey':'PRIVATE_TEST_ONE'}
    r=c.post('/api/settings/ai',json=payload)
    assert r.status_code==200,r.json
    assert 'PRIVATE_TEST' not in r.text
    assert r.json['activeProvider']=='openai'
    item=next(p for p in r.json['providers'] if p['id']=='openai')
    assert item['keyConfigured'] and item['keySource']=='server'
    assert c.get('/api/capabilities').json['analyses']['create'] is True
    rt=app.extensions['evidencetwin']
    assert rt.provider.key=='PRIVATE_TEST_ONE'
    assert stat.S_IMODE(rt.ai_settings.path.stat().st_mode)==0o600
    r=c.post('/api/settings/ai',json={'provider':'openai','model':'changed-model'})
    assert r.status_code==200 and rt.provider.key=='PRIVATE_TEST_ONE'
    assert rt.provider.model=='changed-model'
    c.post('/api/settings/ai',json={**payload,'apiKey':'PRIVATE_TEST_TWO'})
    assert rt.provider.key=='PRIVATE_TEST_TWO'
    r=c.post('/api/settings/ai',json={'provider':'openai','model':'changed-model','removeKey':True})
    assert r.status_code==200
    assert not rt.provider.configured
    assert 'PRIVATE_TEST' not in rt.ai_settings.path.read_text()
    assert not c.get('/api/capabilities').json['analyses']['create']
    assert 'PRIVATE_TEST' not in c.get('/api/settings/ai').text

def test_all_provider_configurations_are_retained_across_switches_and_restart(settings_app):
    app,c=settings_app
    rt=app.extensions['evidencetwin']
    for name in ('ollama','openai','google','anthropic','openrouter','deepseek'):
        r=c.post('/api/settings/ai',json={'provider':name,'model':name+'-test','apiKey':'TEST_ONLY_'+name})
        assert r.status_code==200,r.json
    assert all(p['configured'] for p in c.get('/api/settings/ai').json['providers'])
    directory=rt.store.root
    rt.workflow.shutdown()
    second=create_app({'TESTING':True,'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(directory)})
    try:
        state=second.test_client().get('/api/settings/ai').json
        assert state['activeProvider']=='deepseek'
        assert all(p['configured'] for p in state['providers'])
        assert second.extensions['evidencetwin'].provider.key=='TEST_ONLY_deepseek'
    finally:
        second.extensions['evidencetwin'].workflow.shutdown()

@pytest.mark.parametrize('payload',[
    {'provider':'unknown','model':'x'},
    {'provider':'openai','model':''},
    {'provider':'ollama','model':'x','ollamaHost':'http://untrusted.example'},
    {'provider':'ollama','model':'x','ollamaHost':'https://user:secret@example.com'},
    {'provider':'ollama','model':'x','ollamaHost':'https://example.com/path'},
    {'provider':'openai','model':'x','apiKey':'one','removeKey':True},
    {'provider':'openai','model':'x','apiKey':'\nBAD\nKEY'},
    {'provider':'openai','model':'x','apiKey':'  '},
    {'provider':'openai','model':'x','ollamaHost':'https://ollama.com'},
    {'provider':'openai','model':'x','removeKey':True},
])
def test_invalid_configuration_does_not_overwrite_saved_settings(settings_app,payload):
    app,c=settings_app
    before=c.get('/api/settings/ai').json
    response=c.post('/api/settings/ai',json=payload)
    assert response.status_code==422
    assert c.get('/api/settings/ai').json==before
    assert not app.extensions['evidencetwin'].ai_settings.path.exists()

def test_local_ollama_requires_no_key(settings_app):
    app,c=settings_app
    r=c.post('/api/settings/ai',json={'provider':'ollama','model':'local-test','ollamaHost':'http://127.0.0.1:11434'})
    assert r.status_code==200
    item=r.json['providers'][0]
    assert item['configured'] and not item['requiresKey'] and not item['keyConfigured']
    assert app.extensions['evidencetwin'].provider.configured

def test_model_check_uses_saved_configuration_and_returns_no_key(settings_app,monkeypatch):
    app,c=settings_app
    c.post('/api/settings/ai',json={'provider':'openai','model':'test-model','apiKey':'PRIVATE_TEST_KEY'})
    monkeypatch.setattr(app.extensions['evidencetwin'].provider,'probe',lambda:True)
    r=c.post('/api/settings/ai/test')
    assert r.status_code==200 and r.json['message']=='model_found'
    assert 'PRIVATE_TEST' not in r.text

def test_auth_and_origin_protect_credential_configuration(tmp_path):
    from werkzeug.exceptions import Unauthorized
    def auth():raise Unauthorized()
    app=create_app({'TESTING':True,'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(tmp_path),'AUTHENTICATE_REQUEST':auth})
    c=app.test_client()
    for path in ('/api/settings/ai','/api/settings/ai/test'):
        assert c.post(path,json={}).status_code==401
        assert c.post(path,json={},headers={'Origin':'https://untrusted.example'}).status_code==403
    assert c.get('/api/settings/ai').status_code==401
    app.extensions['evidencetwin'].workflow.shutdown()

def test_environment_key_is_never_returned_and_survives_saved_key_removal(tmp_path):
    app=create_app({'TESTING':True,'RUNTIME_ENABLED':True,'DATA_DIRECTORY':str(tmp_path),'AI_PROVIDER_KEYS':{'openai':'PRIVATE_ENV_KEY'}})
    try:
        c=app.test_client()
        item=next(p for p in c.get('/api/settings/ai').json['providers'] if p['id']=='openai')
        assert item['keySource']=='environment'
        c.post('/api/settings/ai',json={'provider':'openai','model':'test-model','apiKey':'PRIVATE_SAVED_KEY'})
        r=c.post('/api/settings/ai',json={'provider':'openai','model':'test-model','removeKey':True})
        assert next(p for p in r.json['providers'] if p['id']=='openai')['keySource']=='environment'
        assert app.extensions['evidencetwin'].provider.key=='PRIVATE_ENV_KEY'
        assert 'PRIVATE_' not in r.text
    finally:
        app.extensions['evidencetwin'].workflow.shutdown()

def test_inflight_review_keeps_its_initial_provider(settings_app):
    app,c=settings_app
    original=TestProvider();original.block=threading.Event()
    runtime=app.extensions['evidencetwin']
    runtime.provider=runtime.workflow.provider=original
    response=upload(c,metadata(reviewDepth='council'));record_id=response.json['id']
    assert original.started.wait(2)
    try:
        assert c.post('/api/settings/ai',json={'provider':'openai','model':'new-model','apiKey':'PRIVATE_NEW_KEY'}).status_code==200
        original.block.set()
        record=wait(app,record_id)
        assert record['analysis']['status']=='completed_with_limitations'
        assert len(original.calls)==6
        assert all(v.get('provider')==original.name for v in record['reviews'])
        assert runtime.provider.model=='new-model'
    finally:
        original.block.set()
