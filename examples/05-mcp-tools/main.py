import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent

async def main():
    print("=== Example 05: Single MCP Integration ===")
    agent = (
        EnterpriseAgent.builder()
            .use_gemini()
            .register_mcp_server("database_mcp", "http://mcp-server:8080")
            .build()
    )

    res = await agent.chat("Query MCP for user active count.")
    print("Agent Result:", res.value["response"])

if __name__ == "__main__":
    asyncio.run(main())
