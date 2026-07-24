import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent, tool

@tool(name="crm_query", description="Query CRM records")
def crm_query(customer_id: str) -> str:
    return f"CRM Data for {customer_id}: Account Value = $250,000, SLA = Tier 1 Gold"

@tool(name="order_service", description="Fetch customer order records")
def order_service(customer_id: str) -> str:
    return f"Latest orders for {customer_id}: Order #8812 ($12,400, Shipped)"

async def main():
    print("=== Example 15: Production-Ready Blueprint ===")

    agent = (
        EnterpriseAgent.builder()
            .use_azure_openai()
            .use_memory_cache()
            .use_in_memory_bus()
            .register_tool(crm_query)
            .register_tool(order_service)
            .discover_mcp_servers()
            .with_system_prompt("You are a production enterprise AI core agent following SOLID principles.")
            .build()
    )

    query = "Find customer 101 and summarize their last three orders."
    print(f"Executing Query: '{query}'")
    res = await agent.chat(query)

    print("\n--- Execution Output ---")
    print(f"Status: {res.value['status']}")
    print(f"Response:\n{res.value['response']}")
    print(f"Latency: {res.value['execution_time_ms']} ms")
    print("Steps Executed:", len(res.value['steps']))

if __name__ == "__main__":
    asyncio.run(main())
