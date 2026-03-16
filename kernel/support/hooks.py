import logging
from typing import Callable, Any, List, Dict
from kernel.support.exceptions import HookExecutionError

logger = logging.getLogger(__name__)

class HooksRegistry:
    """
    Provides fixed, controllable hook registration and dispatching.
    Used for extension points, not for complex event bussing.
    """
    def __init__(self):
        # Format: { 'hook_name': [{'callback': func, 'order': 100}, ...] }
        self._hooks: Dict[str, List[Dict[str, Any]]] = {}

    def register_hook(self, name: str, callback: Callable, order: int = 100):
        """
        Register a callback to a specific hook name.
        """
        if name not in self._hooks:
            self._hooks[name] = []
            
        self._hooks[name].append({
            'callback': callback,
            'order': order
        })
        # Keep sorted by order (ascending)
        self._hooks[name] = sorted(self._hooks[name], key=lambda x: x['order'])

    def dispatch_hook(self, name: str, payload: Any = None, **kwargs) -> List[Any]:
        """
        Dispatch a hook, calling all registered callbacks in order.
        Returns a list of results from the callbacks.
        """
        if name not in self._hooks:
            return []

        results = []
        for hook in self._hooks[name]:
            callback = hook['callback']
            try:
                result = callback(payload, **kwargs) if payload is not None else callback(**kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Error executing hook '{name}' callback {callback}: {e}", exc_info=True)
                raise HookExecutionError(f"Error in hook '{name}': {str(e)}") from e
                
        return results

    def list_hooks(self, name: str) -> List[Callable]:
        """
        List all callbacks registered for a specific hook name.
        """
        return [hook['callback'] for hook in self.get_raw_hooks(name)]
        
    def get_raw_hooks(self, name: str) -> List[Dict[str, Any]]:
        return self._hooks.get(name, [])

    def clear(self):
        """Clear all registered hooks (mainly for testing)."""
        self._hooks.clear()

# Global singleton for hooks registry
hooks_registry = HooksRegistry()

# Utility functions for easier import
def register_hook(name: str, order: int = 100):
    """Decorator for registering a hook callback."""
    def decorator(func: Callable):
        hooks_registry.register_hook(name, func, order)
        return func
    return decorator

def dispatch_hook(name: str, payload: Any = None, **kwargs) -> List[Any]:
    return hooks_registry.dispatch_hook(name, payload, **kwargs)
