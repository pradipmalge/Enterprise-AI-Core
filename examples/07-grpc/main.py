import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core import EnterpriseAgent
from enterprise_ai_core.grpc.services import GrpcChatService

async def main():
    print("=== Example 07: gRPC Internal Communication Service ===")
    agent = EnterpriseAgent.builder().use_gemini().build()
    grpc_service = GrpcChatService(agent)

    request = {"query": "Execute gRPC internal RPC pipeline."}
    response = await grpc_service.chat_rpc(request)
    print("gRPC Service Response Payload:")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
