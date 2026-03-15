from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from kernel.identity.exceptions import InvalidCredentials, AccountDisabled
from kernel.audit.services.audit_service import AuditService
from kernel.company.services.company_context_service import CompanyContextService

User = get_user_model()

class LoginService:
    @staticmethod
    def login(request, username, password):
        """
        Authenticate and login user.
        """
        user = authenticate(request, username=username, password=password)
        
        # If user is None, auth failed
        if user is None:
            # Try to find if user exists to log detailed failure reason if needed
            # But for security, generic error is better.
            # However, spec asks for AccountDisabled check.
            try:
                existing_user = User.objects.get(username=username)
                if not existing_user.is_active:
                     AuditService.log_login(existing_user, None, request, False, "Account Disabled")
                     raise AccountDisabled()
            except User.DoesNotExist:
                pass
                
            AuditService.log_login(None, None, request, False, "Invalid Credentials")
            raise InvalidCredentials()
            
        if not user.is_active:
             AuditService.log_login(user, None, request, False, "Account Disabled")
             raise AccountDisabled()

        # Perform Django login (session creation)
        login(request, user)
        
        # Log success
        # Try to get default company for audit log context if possible
        company = CompanyContextService.get_current_company(user)
        AuditService.log_login(user, company, request, True)
        
        return user

    @staticmethod
    def logout(request):
        """
        Logout user.
        """
        user = request.user
        if user.is_authenticated:
            # Audit logout
            company = CompanyContextService.get_current_company(user, request)
            AuditService.log_action(user, company, "LOGOUT", str(user))
            
        logout(request)
