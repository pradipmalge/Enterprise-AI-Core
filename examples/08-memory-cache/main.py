import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent

async def main():
    print("=== Example 08: Memory Caching ===")
    agent = EnterpriseAgent.builder().use_gemini().use_memory_cache().build()

    query = "Summarize annual financial projections."
    res1 = await agent.chat(query)
    print("Run 1 (No Cache):", res1.value["execution_time_ms"], "ms")

    res2 = await agent.chat(query)
    print("Run 2 (Cached):", res2.value["execution_time_ms"], "ms (Cached =", res2.value.get("cached", False), ")")

if __name__ == "__main__":
    asyncio.run(main())
