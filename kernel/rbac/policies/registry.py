from __future__ import annotations

from typing import Any, Dict, Type

from .base import BasePolicy


class PolicyRegistry:
    """Policy registry resolving policy by permission code or resource type."""

    _by_code: Dict[str, Type[BasePolicy]] = {}
    _by_resource_type: Dict[str, Type[BasePolicy]] = {}

    @classmethod
    def register_for_code(cls, permission_code: str, policy_class: Type[BasePolicy]) -> None:
        cls._by_code[permission_code] = policy_class

    @classmethod
    def register_for_resource_type(cls, resource_type: str, policy_class: Type[BasePolicy]) -> None:
        cls._by_resource_type[resource_type] = policy_class

    @classmethod
    def resolve(cls, permission_code: str | None = None, resource: Any = None) -> BasePolicy | None:
        if permission_code and permission_code in cls._by_code:
            return cls._by_code[permission_code]()

        resource_type = getattr(resource, 'resource_type', None)
        if resource_type and resource_type in cls._by_resource_type:
            return cls._by_resource_type[resource_type]()

        return None
