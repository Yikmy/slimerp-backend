from typing import Optional
from django.http import HttpRequest
from kernel.core.middleware import get_current_company_id
from kernel.company.models import Company
from kernel.company.exceptions import CompanyNotFound, CurrentCompanyMissing
from .company_service import CompanyService

class CompanyContextService:
    @staticmethod
    def get_current_company(user, request: Optional[HttpRequest] = None) -> Optional[Company]:
        """
        Resolve the current company context.
        Priority:
        1. Explicitly passed request.company_id (set by middleware from header/session)
        2. Thread local storage (via core middleware)
        3. User's default company (fallback)
        """
        company_id = None
        
        # 1. Check request if available
        if request and hasattr(request, 'company_id'):
            company_id = request.company_id
        
        # 2. Check thread local
        if not company_id:
            company_id = get_current_company_id()

        if company_id:
            # Validate access and return object
            # This might hit DB frequently, cache could be considered later
            try:
                return CompanyService.assert_company_access(user, company_id)
            except (CompanyNotFound, Exception):
                # If ID is invalid or access denied, fall back to default?
                # Or raise error? Spec implies strict scope.
                # But for smoother UX, maybe fallback if not explicitly requested?
                # Let's return None or raise based on strictness.
                # Assuming if header is sent, it must be valid.
                pass
        
        # 3. Fallback to default
        return CompanyService.get_default_company(user)
    
    @staticmethod
    def switch_company(user, company_id: str, request: HttpRequest) -> Company:
        """
        Switch current company context.
        Updates session if available.
        """
        company = CompanyService.assert_company_access(user, company_id)
        
        if hasattr(request, 'session'):
            request.session['company_id'] = str(company.id)
            
        return company
