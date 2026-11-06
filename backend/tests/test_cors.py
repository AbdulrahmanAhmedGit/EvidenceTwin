import pytest
from evidencetwin_backend import create_app

@pytest.mark.parametrize('path,method', [('/api/health','GET'),('/api/analyses','GET'),('/api/benchmarks','POST'),('/api/missing','GET')])
def test_allowed_origin_receives_cors_on_success_stubs_and_errors(path,method):
    app=create_app({'TESTING':True,'CORS_ALLOWED_ORIGINS':['http://localhost:5173','http://127.0.0.1:5173']})
    response=app.test_client().open(path,method=method,headers={'Origin':'http://localhost:5173'})
    assert response.headers['Access-Control-Allow-Origin']=='http://localhost:5173'
    assert 'Origin' in response.headers.get('Vary','')
    assert 'Access-Control-Allow-Credentials' not in response.headers

def test_preflight_and_disallowed_origins():
    app=create_app({'TESTING':True,'CORS_ALLOWED_ORIGINS':['http://localhost:5173']})
    client=app.test_client()
    good=client.options('/api/benchmarks',headers={'Origin':'http://localhost:5173','Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'content-type, authorization'})
    assert good.status_code==200 and not good.data
    assert 'POST' in good.headers['Access-Control-Allow-Methods']
    assert 'content-type' in good.headers['Access-Control-Allow-Headers'].lower()
    for origin in ['https://unlisted.example','http://localhost:5173.evil.test','null']:
        denied=client.get('/api/health',headers={'Origin':origin})
        assert 'Access-Control-Allow-Origin' not in denied.headers
    # CORS is a browser policy, not server authorization.
    assert client.get('/api/analyses').status_code==501

def test_default_cors_off(client):
    assert 'Access-Control-Allow-Origin' not in client.get('/api/health',headers={'Origin':'http://localhost:5173'}).headers

@pytest.mark.parametrize('origin',['*','https://*.example.org','https://user:pass@example.org','https://example.org/path','https://example.org?key=test','null'])
def test_unsafe_configuration_fails_at_startup(origin):
    with pytest.raises(ValueError):create_app({'CORS_ALLOWED_ORIGINS':[origin]})

def test_exact_ipv6_origin_is_not_treated_as_a_regular_expression():
    app=create_app({'TESTING':True,'CORS_ALLOWED_ORIGINS':['http://[::1]:5173']})
    response=app.test_client().get('/api/health',headers={'Origin':'http://[::1]:5173'})
    assert response.headers['Access-Control-Allow-Origin']=='http://[::1]:5173'
