from kernel.audit.services.audit_service import AuditService

from kernel.rbac.exceptions import PermissionCodeNotFound, RoleNotFound
from kernel.rbac.models import Permission, Role, RolePermission


class GrantService:
    @staticmethod
    def grant(role_name: str, permission_code: str, actor=None) -> RolePermission:
        """Grant permission to role."""
        role = Role.objects.filter(name=role_name).first()
        if role is None:
            raise RoleNotFound(f'Role {role_name} does not exist')

        permission = Permission.objects.filter(code=permission_code).first()
        if permission is None:
            raise PermissionCodeNotFound(f'Permission {permission_code} does not exist')

        role_permission, _ = RolePermission.objects.get_or_create(role=role, permission=permission)
        AuditService.log_action(
            actor=actor,
            company=None,
            action='rbac.grant',
            target=f'role={role.name}, permission={permission.code}',
            result='ok',
        )
        return role_permission
