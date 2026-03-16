class ConfigException(Exception):
    """Base exception for system config module."""
    pass

class ConfigKeyNotFound(ConfigException):
    """Raised when a requested configuration key is not found."""
    pass

class InvalidConfigValue(ConfigException):
    """Raised when an invalid value is provided for a configuration key."""
    pass
