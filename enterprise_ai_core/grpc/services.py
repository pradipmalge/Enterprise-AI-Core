from typing import Dict, Any
from enterprise_ai_core.common.result import Result

class GrpcChatService:
    def __init__(self, agent):
        self.agent = agent

    async def chat_rpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        query = request.get("query", "")
        res = await self.agent.chat(query)
        if res.is_success:
            return {
                "response": res.value.get("response", ""),
                "status_code": 200,
                "agent_id": res.value.get("agent_id", "")
            }
        return {"response": "", "status_code": 500, "error": res.error}
