import pytest
from django.core.cache import cache
from kernel.system_config.services import config_service
from kernel.system_config.models import SystemConfig, ModuleSwitch, ConfigScope
from kernel.system_config.exceptions import ConfigKeyNotFound
from kernel.company.models import Company

@pytest.fixture
def company(db):
    return Company.objects.create(name="Test Co", code="TC01")

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()

@pytest.mark.django_db
class TestConfigService:

    def test_global_config_get_set(self):
        # Set config
        config_service.set("site_name", "My ERP")
        
        # Get config
        val = config_service.get("site_name")
        assert val == "My ERP"
        
        # Test cache
        cached_val = cache.get(config_service._get_cache_key("site_name", ConfigScope.GLOBAL))
        assert cached_val == "My ERP"

    def test_company_config(self, company):
        config_service.set("tax_rate", "0.1", scope=ConfigScope.COMPANY, company=company)
        
        # Get should work with company
        val = config_service.get("tax_rate", scope=ConfigScope.COMPANY, company=company)
        assert val == "0.1"

        # Global should not have it
        with pytest.raises(ConfigKeyNotFound):
            config_service.get("tax_rate")

    def test_config_not_found_with_default(self):
        val = config_service.get("unknown_key", default="fallback")
        assert val == "fallback"
        
        with pytest.raises(ConfigKeyNotFound):
            config_service.get("unknown_key")

    def test_module_switch(self, company):
        # By default, unknown modules are considered enabled
        assert config_service.is_module_enabled("accounting") == True
        
        # Disable globally
        ModuleSwitch.objects.create(module_name="accounting", is_enabled=False)
        cache.clear()
        assert config_service.is_module_enabled("accounting") == False
        
        # Enable for specific company
        ModuleSwitch.objects.create(module_name="accounting", company=company, is_enabled=True)
        cache.clear()
        
        assert config_service.is_module_enabled("accounting", company=company) == True
        # Global is still false for others
        assert config_service.is_module_enabled("accounting") == False
