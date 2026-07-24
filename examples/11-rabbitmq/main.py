import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent

async def main():
    print("=== Example 11: RabbitMQ Bus Messaging ===")
    agent = EnterpriseAgent.builder().use_gemini().use_rabbitmq_bus().build()
    res = await agent.chat("Publish message to AMQP queue.")
    print("Execution Result:", res.value["status"])

if __name__ == "__main__":
    asyncio.run(main())
