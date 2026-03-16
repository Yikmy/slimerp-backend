import pytest
from kernel.support.hooks import hooks_registry, register_hook, dispatch_hook
from kernel.support.exceptions import HookExecutionError

def test_hooks_registration_and_dispatch():
    hooks_registry.clear()
    
    @register_hook('test_event', order=20)
    def handler_one(payload):
        payload['count'] += 1
        return "one"

    @register_hook('test_event', order=10)
    def handler_two(payload):
        payload['count'] += 2
        return "two"
        
    payload = {'count': 0}
    results = dispatch_hook('test_event', payload=payload)
    
    # handler_two should run first (order=10), then handler_one (order=20)
    # So count should be 0 + 2 + 1 = 3
    assert payload['count'] == 3
    # Results list should maintain order
    assert results == ["two", "one"]

def test_hook_execution_error():
    hooks_registry.clear()
    
    @register_hook('error_event')
    def error_handler():
        raise ValueError("Oops")
        
    with pytest.raises(HookExecutionError):
        dispatch_hook('error_event')

def test_list_hooks():
    hooks_registry.clear()
    
    def h1(): pass
    def h2(): pass
    
    hooks_registry.register_hook('ev', h1)
    hooks_registry.register_hook('ev', h2)
    
    hooks = hooks_registry.list_hooks('ev')
    assert len(hooks) == 2
    assert h1 in hooks
    assert h2 in hooks
