from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from enterprise_ai_core.common.result import Result

@dataclass
class ToolMetadata:
    name: str
    description: str
    parameters: Dict[str, Any]
    required: list = field(default_factory=list)
    version: str = "1.0.0"

class ITool(ABC):
    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> Result[Any]:
        pass
