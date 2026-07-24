import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent

async def main():
    print("=== Example 06: Multiple MCP Servers Discovery ===")
    agent = (
        EnterpriseAgent.builder()
            .use_azure_openai()
            .discover_mcp_servers()
            .build()
    )

    print(f"Registered MCP Clients: {len(agent.mcp_clients)}")
    for client in agent.mcp_clients:
        tools = await client.discover_tools()
        print(f"Server '{client.config.name}' discovered tools: {[t['name'] for t in tools.value]}")

if __name__ == "__main__":
    asyncio.run(main())
