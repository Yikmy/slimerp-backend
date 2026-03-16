from kernel.support.registry import SimpleRegistry
from kernel.support.module_meta import get_installed_modules, get_module_meta

def test_simple_registry():
    reg = SimpleRegistry("test_reg")
    
    reg.register("key1", "val1")
    reg.register("key2", "val2")
    
    assert reg.get("key1") == "val1"
    assert reg.get("key3") is None
    
    all_items = reg.all()
    assert len(all_items) == 2
    
    reg.unregister("key1")
    assert reg.get("key1") is None
    
    reg.clear()
    assert len(reg.all()) == 0

def test_module_meta():
    modules = get_installed_modules()
    assert len(modules) > 0
    
    # Check if a known django app is found
    found_auth = any(m['name'] == 'django.contrib.auth' for m in modules)
    assert found_auth
    
    # Test specific meta
    meta = get_module_meta('support')
    assert meta['name'] == 'kernel.support'
    
    # Test unknown
    unknown_meta = get_module_meta('unknown.app')
    assert unknown_meta == {}
