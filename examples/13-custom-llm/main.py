import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core.llm.interfaces import ILLMProvider
from enterprise_ai_core.common.result import Result
from enterprise_ai_core import EnterpriseAgent

class MyCustomLLM(ILLMProvider):
    async def generate_response(self, prompt, **kwargs):
        return Result.ok({"content": f"[MyCustomLLM Custom Response] processed: '{prompt}'"})

    async def generate_stream(self, prompt, **kwargs):
        yield f"[MyCustomLLM Stream] {prompt}"

async def main():
    print("=== Example 13: Custom LLM Provider ===")
    custom_llm = MyCustomLLM()
    agent = EnterpriseAgent(llm_provider=custom_llm, tool_registry=EnterpriseAgent.builder()._tool_registry)
    res = await agent.chat("Testing custom LLM integration.")
    print("Result:", res.value["response"])

if __name__ == "__main__":
    asyncio.run(main())
