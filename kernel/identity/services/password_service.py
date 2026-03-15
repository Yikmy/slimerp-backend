from kernel.identity.exceptions import PasswordMismatch, InvalidCredentials
from kernel.audit.services.audit_service import AuditService
from kernel.company.services.company_context_service import CompanyContextService

class PasswordService:
    @staticmethod
    def change_password(user, old_password, new_password):
        """
        Change user password.
        """
        if not user.check_password(old_password):
            raise PasswordMismatch()
            
        user.set_password(new_password)
        user.save()
        
        # Audit
        # We need company context for audit, but service methods usually don't take request.
        # Ideally passed in or resolved from thread local if available.
        # Here we assume user has a current company or None.
        company = CompanyContextService.get_current_company(user)
        AuditService.log_action(user, company, "CHANGE_PASSWORD", str(user))
        
        return user
