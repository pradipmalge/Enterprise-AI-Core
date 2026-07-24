from typing import Generic, TypeVar, Optional, List, Any
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    """Standardized enterprise result pattern envelope."""
    is_success: bool
    value: Optional[T] = None
    error: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @classmethod
    def ok(cls, value: T, metadata: Optional[dict] = None) -> 'Result[T]':
        return cls(is_success=True, value=value, metadata=metadata or {})

    @classmethod
    def fail(cls, error: str, errors: Optional[List[str]] = None, metadata: Optional[dict] = None) -> 'Result[T]':
        return cls(is_success=False, error=error, errors=errors or [error], metadata=metadata or {})
