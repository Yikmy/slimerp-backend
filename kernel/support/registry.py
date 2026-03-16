from typing import Dict, Any, Type, Optional

class SimpleRegistry:
    """
    A simple fixed-entry registry.
    Useful for registering services, policies, or components by name.
    """
    def __init__(self, name: str):
        self.name = name
        self._items: Dict[str, Any] = {}

    def register(self, key: str, item: Any):
        """Register an item with a key."""
        if key in self._items:
            # Depending on use case, might want to raise or just warn/overwrite
            # Here we just overwrite, but can be customized
            pass
        self._items[key] = item

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        return self._items.get(key)

    def unregister(self, key: str):
        """Remove an item by key."""
        if key in self._items:
            del self._items[key]

    def all(self) -> Dict[str, Any]:
        """Return all registered items."""
        return self._items.copy()

    def clear(self):
        self._items.clear()
