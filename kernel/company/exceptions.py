from kernel.core.exceptions import BusinessError

class CompanyError(BusinessError):
    """Base class for company module errors."""
    pass

class CompanyNotFound(CompanyError):
    def __init__(self, message="Company not found"):
        super().__init__(message, code="COMPANY_NOT_FOUND")

class CompanyAccessDenied(CompanyError):
    def __init__(self, message="Access to company denied"):
        super().__init__(message, code="COMPANY_ACCESS_DENIED")

class CurrentCompanyMissing(CompanyError):
    def __init__(self, message="Current company context is missing"):
        super().__init__(message, code="CURRENT_COMPANY_MISSING")
