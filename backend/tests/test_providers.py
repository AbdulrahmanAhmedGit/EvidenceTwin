"""Provider wire-format regressions. All remote requests are mocked explicitly."""
from io import BytesIO
import json
from pathlib import Path
import pytest
from PIL import Image
from evidencetwin_backend.config import load_config
from evidencetwin_backend.services.provider import Review, ProviderFailure, OllamaProvider, NoRedirect, validate_references
from evidencetwin_backend.services.transports import make_provider

REVIEW={'agent_id':'visual_analyst','review_status':'insufficient_input','overall_assessment':'Test only.',
        'claim_assessments':[{'claim_id':'c1','position':'cannot_assess','rationale':'Test only.','evidence_refs':['e1']}],
        'findings':[],'limitations':['Test only.'],'missing_information':[],
        'requested_queries':[],'limitation_records':[]}
PACKET={'case_id':'case1','claims':[{'id':'c1','text':'Test'}],'evidence':[{'id':'e1','description':'Test input'}]}

class Reply:
    def __init__(self,data): self.raw=json.dumps(data).encode()
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def read(self,*args): return self.raw

class Transport:
    def __init__(self,reply): self.requests=[];self.reply=reply
    def open(self,request,timeout):
        self.requests.append((request,timeout));return Reply(self.reply)


def envelope(name, content):
    if name=='ollama': return {'done':True,'done_reason':'stop','model':'returned-model','message':{'content':content},'eval_count':3}
    if name=='google': return {'modelVersion':'returned-model','candidates':[{'finishReason':'STOP','content':{'parts':[{'text':content}]}}]}
    if name=='anthropic': return {'model':'returned-model','stop_reason':'end_turn','content':[{'type':'text','text':content}]}
    if name=='openai': return {'model':'returned-model','status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':content}]}]}
    return {'model':'returned-model','choices':[{'finish_reason':'stop','message':{'content':content}}]}

@pytest.mark.parametrize('name',['ollama','openai','google','anthropic','openrouter','deepseek'])
def test_provider_wire_formats(name,tmp_path,monkeypatch):
    monkeypatch.setenv('EVIDENCETWIN_PROVIDER',name);monkeypatch.setenv('EVIDENCETWIN_MODEL','configured-model')
    monkeypatch.setenv(name.upper()+'_API_KEY','test-secret')
    provider=make_provider(load_config());assert provider.configured
    image=tmp_path/'opaque-image-id';Image.new('RGB',(4,3),'white').save(image,format='PNG')
    transport=Transport(envelope(name,json.dumps(REVIEW)))
    module='evidencetwin_backend.services.provider' if name=='ollama' else 'evidencetwin_backend.services.transports'
    monkeypatch.setattr(module+'.build_opener',lambda *args:transport)
    result=provider.chat('visual_analyst',PACKET,[image],Review)
    assert result['data']==REVIEW and result['model']=='returned-model'
    req,timeout=transport.requests[0];body=json.loads(req.data)
    assert timeout==180 and req.method=='POST'
    assert 'test-secret' not in json.dumps(result)
    assert 'test-secret' not in req.full_url and 'test-secret' not in req.data.decode()
    if name=='ollama':
        assert body['messages'][1]['images'];assert 'format' not in body # cloud doesn't guarantee structured output enforcement
    elif name=='google':
        assert body['contents'][0]['parts'][1]['inlineData']['mimeType']=='image/png'
    elif name=='anthropic': assert body['messages'][0]['content'][1]['source']['media_type']=='image/png'
    elif name=='openai':
        assert body['store'] is False and body['input'][0]['content'][1]['image_url'].startswith('data:image/png;base64,')
    else: assert body['messages'][1]['content'][1]['image_url']['url'].startswith('data:image/png;base64,')

@pytest.mark.parametrize('name',['ollama','openai','google','anthropic','openrouter','deepseek'])
def test_provider_invalid_results_are_rejected(name,monkeypatch):
    monkeypatch.setenv('EVIDENCETWIN_PROVIDER',name);monkeypatch.setenv('EVIDENCETWIN_MODEL','configured-model');monkeypatch.setenv(name.upper()+'_API_KEY','test-secret')
    provider=make_provider(load_config());transport=Transport(envelope(name,'{"unexpected":"test-secret"}'))
    module='evidencetwin_backend.services.provider' if name=='ollama' else 'evidencetwin_backend.services.transports'
    monkeypatch.setattr(module+'.build_opener',lambda *args:transport)
    with pytest.raises(ProviderFailure) as exc: provider.chat('visual_analyst',PACKET,[],Review)
    assert 'test-secret' not in str(exc.value)


def test_local_ollama_schema_mode(monkeypatch):
    monkeypatch.setenv('OLLAMA_HOST','http://localhost:11434');monkeypatch.setenv('EVIDENCETWIN_MODEL','configured-model')
    provider=OllamaProvider(load_config());assert provider.configured
    transport=Transport(envelope('ollama',json.dumps(REVIEW)))
    monkeypatch.setattr('evidencetwin_backend.services.provider.build_opener',lambda *args:transport)
    provider.chat('visual_analyst',PACKET,[],Review)
    assert isinstance(json.loads(transport.requests[0][0].data)['format'],dict)

@pytest.mark.parametrize('host',['http://remote.example','https://user:password@example.com','https://example.com/path','file:///tmp/socket'])
def test_provider_host_configuration_is_validated(monkeypatch,host):
    monkeypatch.setenv('OLLAMA_HOST',host)
    with pytest.raises(ValueError):load_config()


def test_redirects_never_forward_credentials():
    assert NoRedirect().redirect_request(None,None,302,'redirect',{},'https://other.example') is None


def test_reference_identity_checks():
    bad={**REVIEW,'agent_id':'scientific_skeptic'}
    with pytest.raises(ProviderFailure):validate_references('visual_analyst',bad,PACKET,{})
    with pytest.raises(ProviderFailure):validate_references('visual_analyst',{**REVIEW,'claim_assessments':[]},PACKET,{})

@pytest.mark.parametrize('name',['openai','google','anthropic','openrouter','deepseek'])
def test_model_probes_use_catalog_endpoints_without_generation(name,monkeypatch):
    monkeypatch.setenv('EVIDENCETWIN_PROVIDER',name)
    monkeypatch.setenv('EVIDENCETWIN_MODEL','test-model')
    monkeypatch.setenv(name.upper()+'_API_KEY','TEST_ONLY_KEY')
    provider=make_provider(load_config())
    payload={'name':'models/test-model'} if name=='google' else {'id':'test-model'} if name in ('openai','anthropic') else {'data':[{'id':'test-model'}]}
    transport=Transport(payload)
    monkeypatch.setattr('evidencetwin_backend.services.transports.build_opener',lambda *args:transport)
    assert provider.probe()
    req,timeout=transport.requests[0]
    assert req.get_method()=='GET' and '/models' in req.full_url and timeout<=10
    assert 'TEST_ONLY_KEY' not in req.full_url
