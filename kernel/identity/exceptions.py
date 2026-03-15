from kernel.core.exceptions import BusinessError

class IdentityError(BusinessError):
    """Base class for identity module errors."""
    pass

class InvalidCredentials(IdentityError):
    def __init__(self, message="Invalid username or password"):
        super().__init__(message, code="INVALID_CREDENTIALS")

class AccountDisabled(IdentityError):
    def __init__(self, message="Account is disabled"):
        super().__init__(message, code="ACCOUNT_DISABLED")

class PasswordMismatch(IdentityError):
    def __init__(self, message="Old password does not match"):
        super().__init__(message, code="PASSWORD_MISMATCH")
