from typing import Dict, List, Any, Optional
from enterprise_ai_core.tools.interfaces import ITool
from enterprise_ai_core.common.result import Result

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ITool] = {}

    def register(self, tool_instance: ITool) -> None:
        name = tool_instance.metadata.name
        self._tools[name] = tool_instance

    def get_tool(self, name: str) -> Optional[ITool]:
        return self._tools.get(name)

    def list_tools(self) -> List[ITool]:
        return list(self._tools.values())

    def get_schemas(self) -> List[Dict[str, Any]]:
        schemas = []
        for t in self._tools.values():
            meta = t.metadata
            schemas.append({
                "name": meta.name,
                "description": meta.description,
                "parameters": meta.parameters,
                "required": meta.required
            })
        return schemas

    async def execute_tool(self, tool_name: str, **kwargs) -> Result[Any]:
        t = self.get_tool(tool_name)
        if not t:
            return Result.fail(f"Tool '{tool_name}' not found in registry.")
        return await t.execute(**kwargs)
