from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List, Optional
from enterprise_ai_core.common.result import Result

class ILLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
    ) -> Result[Dict[str, Any]]:
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        pass
