from typing import Any, Optional
from django.core.cache import cache
from kernel.system_config.models import SystemConfig, ModuleSwitch, ConfigScope
from kernel.system_config.exceptions import ConfigKeyNotFound
from kernel.company.models import Company

class ConfigService:
    """
    Service for unified access to system configurations and module switches.
    Implements caching to reduce database hits.
    """
    
    @staticmethod
    def _get_cache_key(key: str, scope: str, company_id: Optional[int] = None, module: Optional[str] = None) -> str:
        return f"sys_config:{scope}:{company_id or 'none'}:{module or 'none'}:{key}"

    @classmethod
    def get(cls, key: str, scope: str = ConfigScope.GLOBAL, company: Optional[Company] = None, module: Optional[str] = None, default: Any = None) -> Any:
        """
        Get a configuration value.
        Tries to find the specific config based on scope. If not found, falls back to default.
        """
        company_id = company.id if company else None
        cache_key = cls._get_cache_key(key, scope, company_id, module)
        
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        try:
            config = SystemConfig.objects.get(key=key, scope=scope, company=company, module=module)
            cache.set(cache_key, config.value, timeout=3600)  # Cache for 1 hour
            return config.value
        except SystemConfig.DoesNotExist:
            if default is not None:
                return default
            raise ConfigKeyNotFound(f"Configuration key '{key}' not found for scope '{scope}'.")

    @classmethod
    def set(cls, key: str, value: Any, scope: str = ConfigScope.GLOBAL, company: Optional[Company] = None, module: Optional[str] = None, description: str = "") -> SystemConfig:
        """
        Set a configuration value.
        """
        config, created = SystemConfig.objects.update_or_create(
            key=key,
            scope=scope,
            company=company,
            module=module,
            defaults={'value': value, 'description': description}
        )
        
        company_id = company.id if company else None
        cache_key = cls._get_cache_key(key, scope, company_id, module)
        cache.set(cache_key, value, timeout=3600)
        
        return config

    @classmethod
    def is_module_enabled(cls, module_name: str, company: Optional[Company] = None) -> bool:
        """
        Check if a module is enabled.
        If company is provided, checks company-specific switch first, then falls back to global.
        """
        cache_key = f"sys_module_switch:{company.id if company else 'global'}:{module_name}"
        cached_status = cache.get(cache_key)
        
        if cached_status is not None:
            return cached_status

        # Check company specific override
        if company:
            try:
                switch = ModuleSwitch.objects.get(module_name=module_name, company=company)
                cache.set(cache_key, switch.is_enabled, timeout=3600)
                return switch.is_enabled
            except ModuleSwitch.DoesNotExist:
                pass

        # Fallback to global switch
        try:
            switch = ModuleSwitch.objects.get(module_name=module_name, company__isnull=True)
            cache.set(cache_key, switch.is_enabled, timeout=3600)
            return switch.is_enabled
        except ModuleSwitch.DoesNotExist:
            # Modules are enabled by default if not explicitly disabled
            cache.set(cache_key, True, timeout=3600)
            return True

config_service = ConfigService()
