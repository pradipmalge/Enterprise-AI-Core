import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core.tools.interfaces import ITool, ToolMetadata
from enterprise_ai_core.common.result import Result
from enterprise_ai_core import EnterpriseAgent

class CustomClassTool(ITool):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="class_based_analytics",
            description="Run enterprise analytics on datasets",
            parameters={"type": "object", "properties": {"dataset_id": {"type": "string"}}}
        )

    async def execute(self, dataset_id: str = "default", **kwargs) -> Result[str]:
        return Result.ok(f"Class-based tool analytics calculated for dataset '{dataset_id}': Growth +14.2%, Churn -1.1%")

async def main():
    print("=== Example 14: Custom Class-Based Tool ===")
    agent = EnterpriseAgent.builder().use_gemini().register_tool(CustomClassTool()).build()
    res = await agent.chat("Run class_based_analytics on dataset_2026")
    print("Agent Result:", res.value["response"])

if __name__ == "__main__":
    asyncio.run(main())
