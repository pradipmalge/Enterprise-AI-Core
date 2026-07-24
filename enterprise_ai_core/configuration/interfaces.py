from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

class IConfiguration(ABC):
    @abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
