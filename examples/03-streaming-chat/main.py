import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core.chat.engine import ChatEngine
from enterprise_ai_core.llm.gemini_provider import GeminiLLMProvider

async def main():
    print("=== Example 03: Streaming Chat ===")
    llm = GeminiLLMProvider()
    engine = ChatEngine(llm)

    print("Streaming Response:")
    async for chunk in engine.stream_chat("Explain Clean Architecture in AI applications."):
        print(chunk, end="", flush=True)
    print("\n\nStream finished.")

if __name__ == "__main__":
    asyncio.run(main())
