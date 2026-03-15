class BusinessError(Exception):
    """Base class for all business logic errors."""
    def __init__(self, message: str, code: str = "BUSINESS_ERROR", details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

class CoreError(BusinessError):
    """Base class for kernel.core errors."""
    pass
