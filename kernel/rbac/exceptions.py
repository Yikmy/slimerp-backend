from kernel.core.exceptions import BusinessError


class RbacError(BusinessError):
    """Base class for RBAC-related business errors."""


class RoleNotFound(RbacError):
    def __init__(self, message: str = 'Role not found'):
        super().__init__(message=message, code='ROLE_NOT_FOUND')


class PermissionCodeNotFound(RbacError):
    def __init__(self, message: str = 'Permission code not found'):
        super().__init__(message=message, code='PERMISSION_CODE_NOT_FOUND')


class PermissionDenied(RbacError):
    def __init__(self, message: str = 'Permission denied', details: dict | None = None):
        super().__init__(message=message, code='PERMISSION_DENIED', details=details or {})
