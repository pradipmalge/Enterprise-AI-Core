import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent, tool

@tool(name="order_history", description="Fetch order history for a given customer")
def get_orders(customer_id: str) -> str:
    return f"Orders for {customer_id}: ORD-9901 (Shipped), ORD-9902 (Delivered), ORD-9903 (Processing)"

async def main():
    print("=== Example 02: FastAPI / Web API Integration ===")
    agent = (
        EnterpriseAgent.builder()
            .use_azure_openai()
            .use_memory_cache()
            .register_tool(get_orders)
            .build()
    )

    response = await agent.chat("Find customer 101 and summarize their last three orders.")
    print("FastAPI Response Endpoint Output:")
    print(response.value)

if __name__ == "__main__":
    asyncio.run(main())
