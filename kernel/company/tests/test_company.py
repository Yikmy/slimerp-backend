import pytest
from django.contrib.auth import get_user_model
from kernel.company.models import Company, UserCompanyAccess
from kernel.company.services.company_service import CompanyService
from kernel.company.services.company_context_service import CompanyContextService
from kernel.company.exceptions import CompanyNotFound, CompanyAccessDenied

User = get_user_model()

@pytest.mark.django_db
class TestCompanyService:
    def test_create_company(self):
        user = User.objects.create_user(username='testuser', password='password')
        company = CompanyService.create_company(name="Test Corp", code="TEST", creator_user=user)
        
        assert company.name == "Test Corp"
        assert UserCompanyAccess.objects.filter(user=user, company=company).exists()
        assert UserCompanyAccess.objects.get(user=user, company=company).is_default

    def test_access_control(self):
        user = User.objects.create_user(username='user2', password='password')
        company = CompanyService.create_company(name="No Access Corp", code="NOACC")
        
        with pytest.raises(CompanyAccessDenied):
            CompanyService.assert_company_access(user, company.id)
            
        UserCompanyAccess.objects.create(user=user, company=company)
        assert CompanyService.assert_company_access(user, company.id) == company

@pytest.mark.django_db
class TestCompanyContext:
    def test_switch_company(self):
        user = User.objects.create_user(username='context_user', password='password')
        c1 = CompanyService.create_company(name="C1", code="C1", creator_user=user)
        c2 = CompanyService.create_company(name="C2", code="C2", creator_user=user)
        
        # Mock request with session
        class MockRequest:
            def __init__(self, u):
                self.session = {}
                self.user = u
            
        req = MockRequest(user)
        
        # Switch to C2
        CompanyContextService.switch_company(user, c2.id, req)
        assert req.session['company_id'] == str(c2.id)
        
        # Get context from session (simulated)
        req.company_id = req.session['company_id']
        current = CompanyContextService.get_current_company(user, req)
        assert current == c2

@pytest.mark.django_db
class TestCompanyAPI:
    def test_list_companies(self, client):
        user = User.objects.create_user(username='api_user', password='password')
        c1 = CompanyService.create_company(name="API C1", code="AC1", creator_user=user)
        client.force_login(user)
        
        resp = client.get('/api/v1/companies/')
        assert resp.status_code == 200
        assert len(resp.data['data']) == 1
        assert resp.data['data'][0]['code'] == "AC1"
