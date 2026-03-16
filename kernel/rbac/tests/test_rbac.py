import pytest
from django.contrib.auth import get_user_model

from kernel.company.services.company_service import CompanyService
from kernel.rbac.models import Permission, Role, RolePermission, UserRole
from kernel.rbac.policies.base import BasePolicy, PolicyResult
from kernel.rbac.policies.registry import PolicyRegistry
from kernel.rbac.services.permission_service import PermissionService

User = get_user_model()


class DenyAllPolicy(BasePolicy):
    def evaluate(self, *, user, company, resource, action):
        return PolicyResult(allowed=False, reason='blocked_by_policy')


@pytest.mark.django_db
class TestPermissionService:
    def test_basic_permission_hit(self):
        user = User.objects.create_user(username='rbac_u1', password='password')
        company = CompanyService.create_company(name='RBAC C1', code='RBAC1', creator_user=user)
        role = Role.objects.create(name='viewer')
        perm = Permission.objects.create(code='sales.order.read')

        UserRole.objects.create(user=user, company=company, role=role)
        RolePermission.objects.create(role=role, permission=perm)

        result = PermissionService.has_perm(user=user, company=company, code='sales.order.read')
        assert result.allowed is True
        assert result.reason == 'ok'

    def test_company_scope_isolation(self):
        user = User.objects.create_user(username='rbac_u2', password='password')
        c1 = CompanyService.create_company(name='Scope C1', code='SC1', creator_user=user)
        c2 = CompanyService.create_company(name='Scope C2', code='SC2', creator_user=user)
        role = Role.objects.create(name='editor')
        perm = Permission.objects.create(code='inventory.item.update')

        UserRole.objects.create(user=user, company=c1, role=role)
        RolePermission.objects.create(role=role, permission=perm)

        assert PermissionService.has_perm(user=user, company=c1, code=perm.code).allowed is True
        result_c2 = PermissionService.has_perm(user=user, company=c2, code=perm.code)
        assert result_c2.allowed is False
        assert result_c2.reason == 'not_granted'

    def test_policy_denies_after_grant(self):
        user = User.objects.create_user(username='rbac_u3', password='password')
        company = CompanyService.create_company(name='Policy C1', code='PC1', creator_user=user)
        role = Role.objects.create(name='approver')
        perm = Permission.objects.create(code='finance.invoice.approve')
        UserRole.objects.create(user=user, company=company, role=role)
        RolePermission.objects.create(role=role, permission=perm)

        PolicyRegistry.register_for_code('finance.invoice.approve', DenyAllPolicy)

        result = PermissionService.has_perm(
            user=user,
            company=company,
            code='finance.invoice.approve',
            resource={'id': 'inv-1'},
        )
        assert result.allowed is False
        assert result.reason == 'blocked_by_policy'


@pytest.mark.django_db
class TestRbacAPI:
    def test_me_permissions_endpoint(self, client):
        user = User.objects.create_user(username='rbac_api', password='password')
        company = CompanyService.create_company(name='API RBAC Co', code='RAPI', creator_user=user)
        role = Role.objects.create(name='api_viewer')
        perm = Permission.objects.create(code='crm.customer.read')

        UserRole.objects.create(user=user, company=company, role=role)
        RolePermission.objects.create(role=role, permission=perm)

        client.force_login(user)
        resp = client.get(f'/api/v1/rbac/me-permissions/?company_id={company.id}')

        assert resp.status_code == 200
        assert len(resp.data['data']) == 1
        assert resp.data['data'][0]['code'] == 'crm.customer.read'
