from abc import ABC, abstractmethod
from typing import Callable, Any, Dict

class IMessageBus(ABC):
    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        pass
