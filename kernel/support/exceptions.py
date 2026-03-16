class SupportException(Exception):
    """Base exception for support module."""
    pass

class HookNotFound(SupportException):
    """Raised when an unregistered hook is called or queried, if strict checking is needed."""
    pass

class HookExecutionError(SupportException):
    """Raised when a hook callback execution fails."""
    pass


class RegistryKeyError(SupportException):
    """Raised when attempting invalid key operations in registries."""
    pass
