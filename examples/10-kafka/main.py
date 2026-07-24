import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent

async def main():
    print("=== Example 10: Kafka Event Bus Messaging ===")
    agent = EnterpriseAgent.builder().use_gemini().use_kafka_bus("localhost:9092").build()

    async def on_event(msg):
        print(f"Received Kafka Event: {msg['event_type']} -> {msg['payload']['query']}")

    await agent.bus.subscribe("agent.completed", on_event)
    await agent.chat("Publish message to Kafka event pipeline.")

if __name__ == "__main__":
    asyncio.run(main())
