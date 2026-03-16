from dataclasses import dataclass

from kernel.rbac.exceptions import PermissionCodeNotFound
from kernel.rbac.models import Permission, RolePermission, UserRole
from kernel.rbac.policies import PolicyRegistry


@dataclass
class PermissionCheckResult:
    allowed: bool
    reason: str


class PermissionService:
    @staticmethod
    def has_perm(user, company, code: str, resource=None) -> PermissionCheckResult:
        """Check permission with role grants and optional policy guard."""
        permission = Permission.objects.filter(code=code).first()
        if permission is None:
            raise PermissionCodeNotFound(f'Permission {code} does not exist')

        user_role_ids = UserRole.objects.filter(user=user, company=company).values_list('role_id', flat=True)
        granted = RolePermission.objects.filter(role_id__in=user_role_ids, permission=permission).exists()
        if not granted:
            return PermissionCheckResult(allowed=False, reason='not_granted')

        action = code.split('.')[-1]
        policy = PolicyRegistry.resolve(permission_code=code, resource=resource)
        if policy is None:
            return PermissionCheckResult(allowed=True, reason='ok')

        policy_result = policy.evaluate(user=user, company=company, resource=resource, action=action)
        if not policy_result.allowed:
            return PermissionCheckResult(allowed=False, reason=policy_result.reason or 'policy_denied')

        return PermissionCheckResult(allowed=True, reason='ok')
