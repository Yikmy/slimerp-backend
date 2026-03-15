from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from kernel.core.api.responses import success_response, error_response
from kernel.company.services.company_service import CompanyService
from kernel.company.services.company_context_service import CompanyContextService
from kernel.company.api.serializers import CompanySerializer, CompanySwitchSerializer
from kernel.company.exceptions import CompanyNotFound, CompanyAccessDenied

class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List companies accessible by the user."""
        companies = CompanyService.get_user_companies(request.user)
        serializer = CompanySerializer(companies, many=True)
        return success_response(data=serializer.data)

class CurrentCompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current company context."""
        company = CompanyContextService.get_current_company(request.user, request)
        if not company:
            # Maybe return empty or default? Or error?
            # If user has no company access at all.
            return success_response(data=None, message="No company context active")
            
        serializer = CompanySerializer(company)
        return success_response(data=serializer.data)

class SwitchCompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Switch current company session."""
        serializer = CompanySwitchSerializer(data=request.data)
        if serializer.is_valid():
            company_id = serializer.validated_data['company_id']
            try:
                company = CompanyContextService.switch_company(request.user, company_id, request)
                return success_response(message=f"Switched to {company.name}")
            except (CompanyNotFound, CompanyAccessDenied) as e:
                return error_response(message=str(e), code=e.code, status=403)
        return error_response(message="Invalid data", data=serializer.errors)
