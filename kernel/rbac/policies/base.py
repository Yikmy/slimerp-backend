from dataclasses import dataclass
from typing import Any


@dataclass
class PolicyResult:
    allowed: bool
    reason: str = ''


class BasePolicy:
    """Base interface for resource-level policy checks."""

    def evaluate(self, *, user: Any, company: Any, resource: Any, action: str) -> PolicyResult:
        return PolicyResult(allowed=True)
