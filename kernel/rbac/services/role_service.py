from kernel.audit.services.audit_service import AuditService
from kernel.company.models import Company
from kernel.company.exceptions import CompanyNotFound

from kernel.rbac.exceptions import RoleNotFound
from kernel.rbac.models import Role, UserRole


class RoleService:
    @staticmethod
    def assign_role(user, company_id: str, role_name: str, actor=None) -> UserRole:
        """Assign a role to user in company scope."""
        company = Company.objects.filter(id=company_id).first()
        if company is None:
            raise CompanyNotFound(f'Company {company_id} does not exist')

        role = Role.objects.filter(name=role_name).first()
        if role is None:
            raise RoleNotFound(f'Role {role_name} does not exist')

        user_role, _ = UserRole.objects.get_or_create(user=user, company=company, role=role)
        AuditService.log_action(
            actor=actor,
            company=company,
            action='rbac.assign_role',
            target=f'user={user.id}, role={role.name}',
            result='ok',
        )
        return user_role
