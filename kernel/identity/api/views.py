from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from kernel.core.api.responses import success_response, error_response
from kernel.identity.services.login_service import LoginService
from kernel.identity.services.session_service import SessionService
from kernel.identity.services.password_service import PasswordService
from kernel.identity.api.serializers import LoginSerializer, ChangePasswordSerializer, MeResponseSerializer
from kernel.company.services.company_context_service import CompanyContextService

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # This service handles authentication and raises BusinessError on failure
            user = LoginService.login(request, username, password)
            
            # Handle session attachment (placeholder per spec)
            resp = success_response(message="Login successful")
            SessionService.attach_session(resp, user)
            
            return resp
        return error_response("Invalid data", data=serializer.errors)

class LogoutView(APIView):
    permission_classes = [AllowAny] # Or IsAuthenticated? Logout can be called by anyone technically.

    def post(self, request):
        LoginService.logout(request)
        return success_response(message="Logged out successfully")

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        current_company = CompanyContextService.get_current_company(user, request)
        
        # Roles placeholder - RBAC not implemented fully yet
        roles = [] 
        if hasattr(user, 'roles'): # Maybe future implementation
             roles = [r.code for r in user.roles.all()]

        data = {
            "user": user,
            "current_company": current_company,
            "roles": roles
        }
        
        serializer = MeResponseSerializer(data)
        return success_response(data=serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old = serializer.validated_data['old_password']
            new = serializer.validated_data['new_password']
            
            PasswordService.change_password(request.user, old, new)
            
            # Changing password usually invalidates other sessions, 
            # Django's update_session_auth_hash is needed if we want to keep current session alive.
            # But spec didn't mention it. Let's assume standard behavior.
            # If we want to keep logged in:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            return success_response(message="Password changed successfully")
        return error_response("Invalid data", data=serializer.errors)
