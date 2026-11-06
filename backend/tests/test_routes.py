from io import BytesIO
import inspect
import pytest
from flask import request
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from evidencetwin_backend import create_app
from evidencetwin_backend.catalog import OPERATIONS
from evidencetwin_backend.contracts.common import validate_contract
from evidencetwin_backend.contracts.system import HealthResponse, CapabilitiesResponse
from evidencetwin_backend.errors import ErrorResponse

EXPECTED = {
    ('GET','/health'), ('GET','/capabilities'), ('GET','/activity'),
    ('GET','/analyses'), ('POST','/analyses'), ('GET','/analyses/<analysis_id>'),
    ('DELETE','/analyses/<analysis_id>'), ('POST','/analyses/<analysis_id>/retry'),
    ('POST','/analyses/<analysis_id>/cancel'), ('GET','/analyses/<analysis_id>/evidence'),
    ('GET','/analyses/<analysis_id>/dataset'), ('GET','/analyses/<analysis_id>/visualizations'),
    ('GET','/analyses/<analysis_id>/council'), ('GET','/analyses/<analysis_id>/audit'),
    ('GET','/analyses/<analysis_id>/report'), ('GET','/comparisons'),
    ('GET','/benchmarks'), ('POST','/benchmarks'), ('GET','/benchmarks/<benchmark_id>'),
    ('GET','/reports'), ('GET','/reports/<report_id>'), ('DELETE','/reports/<report_id>'),
    ('GET','/integrations'), ('POST','/integrations/<integration_id>/test'),
    ('GET','/cases'), ('GET','/cases/<case_id>'),
}

def url(operation):
    path = '/api' + operation.path
    for key in ['analysis_id','benchmark_id','report_id','integration_id','case_id']:
        path = path.replace('<'+key+'>', 'contract-test-id')
    return path

def test_factory_instances_and_all_blueprints():
    first = create_app({'TESTING':True})
    second = create_app({'TESTING':True})
    assert first is not second
    assert set(first.blueprints) == {'system','analyses','evidence','visualizations','council','audit','reports','comparisons','benchmarks','integrations','cases'}
    assert first.static_folder is None

def test_inventory_and_actual_methods_match(app):
    expected = {(method, '/api'+path) for method,path in EXPECTED}
    actual = {(method,rule.rule) for rule in app.url_map.iter_rules() for method in rule.methods-{'HEAD','OPTIONS'}}
    assert actual == expected
    assert {(op.method, '/api'+op.path) for op in OPERATIONS} == expected
    assert len([op for op in OPERATIONS if op.blueprint!='cases']) == 24
    assert len(OPERATIONS) == 26

@pytest.mark.parametrize('operation',OPERATIONS,ids=lambda op:op.blueprint+'.'+op.function)
def test_registered_operations_are_truthful(app, client, operation):
    response = client.open(url(operation), method=operation.method)
    assert response.status_code == operation.status
    assert response.is_json
    assert response.headers['Cache-Control'] == 'no-store'
    if operation.status == 501:
        payload = validate_contract(ErrorResponse,response.json)
        assert set(payload) == {'error'}
        assert payload['error']['code'] == 'not_implemented'
        assert payload['error']['operation'] == operation.blueprint+'.'+operation.function
        assert 'not implemented' in payload['error']['message']
        handler = app.view_functions[operation.blueprint+'.'+operation.function]
        doc = inspect.getdoc(handler)
        assert 'TODO (OWNER)' in doc and 'Input:' in doc and 'Output:' in doc and 'Frontend consumer:' in doc
        assert handler.__annotations__['return'].__name__ == 'Response'

@pytest.mark.parametrize('operation',OPERATIONS,ids=lambda op:op.function)
def test_automatic_options_only_negotiates_methods(client, operation):
    response = client.options(url(operation))
    assert response.status_code == 200
    assert not response.data
    assert operation.method in response.headers['Allow']

@pytest.mark.parametrize('operation',[op for op in OPERATIONS if op.method=='GET'],ids=lambda op:op.function)
def test_head_has_no_body_and_retains_operation_status(client, operation):
    response = client.head(url(operation))
    assert response.status_code == operation.status
    assert not response.data

def test_health_is_only_liveness(client):
    value = validate_contract(HealthResponse,client.get('/api/health').json)
    assert value['status']=='ok'
    assert value['mode']=='integration_skeleton'
    assert value['scientificServices']=='unavailable'
    assert set(value)=={'status','apiVersion','mode','scientificServices'}

def test_all_scientific_capabilities_remain_disabled(client):
    value = validate_contract(CapabilitiesResponse,client.get('/api/capabilities').json)
    assert value['providers']==[] and value['activity'] is False
    assert value['jobAvailability']=='unavailable'
    assert value['analyses']=={'create':False,'delete':False,'retry':False,'maxClaims':1,'modes':[],'reviewDepths':[]}
    assert value['research']=={'comparison':False,'benchmarks':{'read':False,'create':False},'reports':{'read':False},'integrations':{'read':False}}
    assert all(service['status']=='unavailable' for service in value['services'])

@pytest.mark.parametrize('path,method,status,code',[
    ('/api/unknown','GET',404,'not_found'),('/api/analyses','PUT',405,'method_not_allowed'),
    ('/api/mcp','GET',404,'not_found'),('/api/analyses/id/status','GET',404,'not_found'),
    ('/api/analyses/id/events','GET',404,'not_found'),
])
def test_unknown_routes_and_methods_use_json(client,path,method,status,code):
    response = client.open(path,method=method)
    assert response.status_code==status
    assert validate_contract(ErrorResponse,response.json)['error']['code']==code
    if status==405:assert 'POST' in response.headers['Allow']

def test_errors_never_echo_payloads_or_exceptions(app,caplog):
    @app.get('/api/_test-error')
    def fail():
        raise RuntimeError('PRIVATE_TEST_VALUE')
    response=app.test_client().get('/api/_test-error?token=PRIVATE_TEST_VALUE')
    assert response.status_code==500
    assert response.json['error']['code']=='internal_error'
    assert 'PRIVATE_TEST_VALUE' not in response.text
    assert 'PRIVATE_TEST_VALUE' not in caplog.text

def test_upload_is_not_accepted_or_written(client,tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    response=client.post('/api/analyses',data={'metadata':'{"claim":"Input contract only"}','files':(BytesIO(b'input'),'chart.png')})
    assert response.status_code==501 and response.json['error']['code']=='not_implemented'
    assert list(tmp_path.iterdir())==[]
    # Unavailable operations do not claim to validate or accept malformed payloads.
    assert client.post('/api/benchmarks',data='{broken',content_type='application/json').status_code==501

def test_body_size_limit_is_json_before_stub_execution():
    app=create_app({'TESTING':True,'MAX_CONTENT_LENGTH':32})
    response=app.test_client().post('/api/analyses',data=b'x'*33)
    assert response.status_code==413
    assert response.json['error']['code']=='request_too_large'

def test_form_parser_limits_are_configured_and_apply_when_owner_parses(app):
    app.config['MAX_FORM_MEMORY_SIZE']=16
    @app.post('/api/_test-parser')
    def parse():
        return dict(request.form)
    response=app.test_client().post('/api/_test-parser',data={'metadata':'x'*32},content_type='multipart/form-data')
    assert response.status_code==413 and response.json['error']['code']=='request_too_large'
    assert app.config['MAX_FORM_PARTS']==32

@pytest.mark.parametrize('error,status,code',[(Unauthorized,401,'authorization_required'),(Forbidden,403,'access_denied'),(BadRequest,400,'bad_request')])
def test_owner_auth_hook_uses_existing_error_schema(error,status,code):
    def authenticate():raise error('PRIVATE_TEST_VALUE')
    app=create_app({'TESTING':True,'AUTHENTICATE_REQUEST':authenticate})
    client=app.test_client()
    response=client.get('/api/analyses')
    assert response.status_code==status and response.json['error']['code']==code
    assert 'PRIVATE_TEST_VALUE' not in response.text
    assert client.get('/api/health').status_code==200
    assert client.get('/api/capabilities').status_code==200
    assert client.options('/api/analyses').status_code==200

def test_supplied_bearer_does_not_create_fake_authentication(client):
    response=client.get('/api/analyses',headers={'Authorization':'Bearer CONTRACT_TEST_ONLY'})
    assert response.status_code==501
    assert 'CONTRACT_TEST_ONLY' not in response.text

@pytest.mark.parametrize('result',[False,{'user':'not-an-authenticator'}])
def test_auth_hook_invalid_return_fails_closed(result):
    app=create_app({'TESTING':True,'AUTHENTICATE_REQUEST':lambda:result})
    response=app.test_client().get('/api/analyses')
    assert response.status_code==500 and response.json['error']['code']=='internal_error'

@pytest.mark.parametrize('key',['MAX_CONTENT_LENGTH','MAX_FORM_MEMORY_SIZE','MAX_FORM_PARTS'])
def test_transport_limits_cannot_silently_be_disabled(key):
    with pytest.raises(ValueError):create_app({key:None})

def test_environment_configuration_is_loaded_without_advertising_science(monkeypatch):
    monkeypatch.setenv('EVIDENCETWIN_MAX_CONTENT_LENGTH','32')
    monkeypatch.setenv('EVIDENCETWIN_CORS_ORIGINS','http://localhost:5173')
    app=create_app({'TESTING':True})
    client=app.test_client()
    assert client.post('/api/analyses',data=b'x'*33).status_code==413
    assert client.get('/api/health',headers={'Origin':'http://localhost:5173'}).headers['Access-Control-Allow-Origin']=='http://localhost:5173'
    assert client.get('/api/capabilities').json['analyses']['create'] is False

def test_collection_trailing_slashes_do_not_redirect_post_bodies(client):
    response=client.post('/api/analyses/',data={'metadata':'{}'})
    assert response.status_code==501 and 'Location' not in response.headers

def test_multipart_part_count_limit_applies_when_owner_parses(app):
    app.config['MAX_FORM_PARTS']=2
    @app.post('/api/_test-parts')
    def parse():return dict(request.form)
    response=app.test_client().post('/api/_test-parts',data={'a':'1','b':'2','c':'3'},content_type='multipart/form-data')
    assert response.status_code==413 and response.json['error']['code']=='request_too_large'
