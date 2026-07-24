import asyncio
import sys
import os

# Add package root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent, tool

@tool(name="customer_search", description="Search customer database by ID or Name")
def customer_search(query: str) -> str:
    return f"Customer record found for '{query}': ID=101, Name=Acme Corp, Tier=Enterprise, Status=Active"

async def main():
    print("=== Enterprise AI Core Example 01: Console Chat ===")
    agent = (
        EnterpriseAgent.builder()
            .use_gemini()
            .use_memory_cache()
            .use_in_memory_bus()
            .register_tool(customer_search)
            .build()
    )

    query = "Find customer 101 and summarize their status."
    print(f"\nUser Query: {query}")
    result = await agent.chat(query)

    if result.is_success:
        print(f"\nAgent Response:\n{result.value['response']}")
        print(f"\nExecution Latency: {result.value['execution_time_ms']} ms")
    else:
        print(f"Error: {result.error}")

if __name__ == "__main__":
    asyncio.run(main())
