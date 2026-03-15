import pytest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from kernel.core.middleware import CurrentCompanyMiddleware, get_current_company_id

@pytest.fixture
def middleware():
    return CurrentCompanyMiddleware(lambda request: None)

@pytest.fixture
def factory():
    return RequestFactory()

def test_company_middleware_header(middleware, factory):
    request = factory.get('/')
    request.headers = {'X-Company-ID': 'test-uuid'}
    
    middleware.process_request(request)
    
    assert request.company_id == 'test-uuid'
    assert get_current_company_id() == 'test-uuid'
    
    middleware.process_response(request, None)
    assert get_current_company_id() is None

def test_company_middleware_session(middleware, factory):
    request = factory.get('/')
    # Simulate session
    class MockSession(dict):
        pass
    request.session = MockSession({'company_id': 'session-uuid'})
    
    middleware.process_request(request)
    
    assert request.company_id == 'session-uuid'
    assert get_current_company_id() == 'session-uuid'
    
    middleware.process_response(request, None)

def test_company_middleware_none(middleware, factory):
    request = factory.get('/')
    if hasattr(request, 'headers'):
         # RequestFactory creates headers but we want to ensure empty for this key
         pass
    
    middleware.process_request(request)
    
    assert request.company_id is None
    assert get_current_company_id() is None
