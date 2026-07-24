import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent, tool

@tool(name="weather_tool", description="Get current weather for location")
def weather_tool(location: str) -> str:
    return f"Weather in {location}: 22°C, Clear Sky, Humidity 45%"

@tool(name="calc_tool", description="Perform calculation")
def calc_tool(expression: str) -> str:
    return f"Calculated '{expression}' = 42"

async def main():
    print("=== Example 04: Local Tools Registration ===")
    agent = (
        EnterpriseAgent.builder()
            .use_gemini()
            .register_tool(weather_tool)
            .register_tool(calc_tool)
            .build()
    )

    res = await agent.chat("What's the weather in Tokyo?")
    print("Agent Result:", res.value["response"])

if __name__ == "__main__":
    asyncio.run(main())
