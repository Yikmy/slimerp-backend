from django.apps import apps
from typing import Dict, Any, List

def get_installed_modules() -> List[Dict[str, Any]]:
    """
    Retrieve metadata about installed modules (Django apps).
    Can be used by config_service or UI to list available modules.
    """
    modules = []
    for app_config in apps.get_app_configs():
        modules.append({
            "name": app_config.name,
            "label": app_config.label,
            "verbose_name": app_config.verbose_name,
        })
    return modules

def get_module_meta(module_name: str) -> Dict[str, Any]:
    """
    Get metadata for a specific module.
    """
    try:
        app_config = apps.get_app_config(module_name)
        return {
            "name": app_config.name,
            "label": app_config.label,
            "verbose_name": app_config.verbose_name,
        }
    except LookupError:
        return {}
