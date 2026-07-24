from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IMemoryProvider(ABC):
    @abstractmethod
    async def add_message(self, session_id: str, role: str, content: str) -> None:
        pass

    @abstractmethod
    async def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def clear(self, session_id: str) -> None:
        pass
