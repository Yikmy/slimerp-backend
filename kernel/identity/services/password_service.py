from kernel.identity.exceptions import PasswordMismatch, InvalidCredentials
from kernel.audit.services.audit_service import AuditService

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
        AuditService.log_action(user, None, "CHANGE_PASSWORD", str(user))
        
        return user
