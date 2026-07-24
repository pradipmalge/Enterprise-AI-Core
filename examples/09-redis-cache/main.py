import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent

async def main():
    print("=== Example 09: Redis Cache Integration ===")
    agent = EnterpriseAgent.builder().use_azure_openai().use_redis_cache("redis://localhost:6379/0").build()
    res = await agent.chat("Check cache efficiency.")
    print("Agent Response:", res.value["response"])

if __name__ == "__main__":
    asyncio.run(main())
