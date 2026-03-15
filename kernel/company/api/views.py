from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from kernel.core.api.responses import success_response, error_response
from kernel.company.services.company_service import CompanyService
from kernel.company.api.serializers import CompanySerializer, CompanySwitchSerializer
from kernel.company.exceptions import CompanyNotFound, CompanyAccessDenied

class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List companies accessible by the user."""
        companies = CompanyService.get_user_companies(request.user)
        serializer = CompanySerializer(companies, many=True)
        return success_response(data=serializer.data)

class VerifyCompanyAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Verify access to a company."""
        serializer = CompanySwitchSerializer(data=request.data)
        if serializer.is_valid():
            company_id = serializer.validated_data['company_id']
            try:
                company = CompanyService.assert_company_access(request.user, company_id)
                company_data = CompanySerializer(company).data
                return success_response(data={"has_access": True, "company_info": company_data})
            except (CompanyNotFound, CompanyAccessDenied) as e:
                return error_response(message=str(e), code="ACCESS_DENIED", status=403)
        return error_response(message="Invalid data", data=serializer.errors)
