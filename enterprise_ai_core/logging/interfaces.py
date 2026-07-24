from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

class ILogger(ABC):
    @abstractmethod
    def info(self, msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def error(self, msg: str, exc: Optional[Exception] = None, context: Optional[Dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def debug(self, msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        pass
