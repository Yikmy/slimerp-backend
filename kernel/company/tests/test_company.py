import pytest
from django.contrib.auth import get_user_model
from kernel.company.models import Company, UserCompanyAccess
from kernel.company.services.company_service import CompanyService
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

    def test_user_has_company(self):
        user = User.objects.create_user(username='user3', password='password')
        company = CompanyService.create_company(name="Check Access Corp", code="CHKACC")
        
        assert not CompanyService.user_has_company(user, company.id)
        
        UserCompanyAccess.objects.create(user=user, company=company)
        assert CompanyService.user_has_company(user, company.id)

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

    def test_verify_company_access(self, client):
        user = User.objects.create_user(username='verify_user', password='password')
        c1 = CompanyService.create_company(name="Verify C1", code="VC1", creator_user=user)
        c2 = CompanyService.create_company(name="Verify C2", code="VC2") # No access
        client.force_login(user)
        
        # Verify access to C1
        resp = client.post('/api/v1/companies/verify/', {'company_id': c1.id})
        assert resp.status_code == 200
        assert resp.data['data']['has_access'] is True
        
        # Verify access to C2
        resp = client.post('/api/v1/companies/verify/', {'company_id': c2.id})
        assert resp.status_code == 403
