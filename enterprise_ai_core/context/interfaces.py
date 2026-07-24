from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from .models import ContextFragment, ContextEnvelope

class IContextProvider(ABC):
    """Interface for dynamic context providers contributing prompt fragments."""
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        pass

class IContextTransformer(ABC):
    """Interface for context transformation pipeline steps."""
    @abstractmethod
    async def transform(self, envelope: ContextEnvelope) -> ContextEnvelope:
        pass

class IContextFilter(ABC):
    """Interface for filtering sensitive data, PII, or unsafe elements."""
    @abstractmethod
    async def filter(self, envelope: ContextEnvelope) -> ContextEnvelope:
        pass

class IContextOptimizer(ABC):
    """Interface for optimizing and fitting context into token budgets."""
    @abstractmethod
    async def optimize(self, envelope: ContextEnvelope, max_tokens: int) -> ContextEnvelope:
        pass

class IContextStore(ABC):
    """Interface for persisting and retrieving context state."""
    @abstractmethod
    async def save(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
