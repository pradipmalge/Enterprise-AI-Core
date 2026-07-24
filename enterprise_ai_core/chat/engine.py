import uuid
from typing import AsyncGenerator, Dict, Any, List, Optional
from enterprise_ai_core.llm.interfaces import ILLMProvider
from enterprise_ai_core.memory.interfaces import IMemoryProvider
from enterprise_ai_core.common.result import Result

class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)

class ChatEngine:
    def __init__(
        self,
        llm_provider: ILLMProvider,
        memory_provider: Optional[IMemoryProvider] = None,
        system_prompt: str = "You are an enterprise AI assistant."
    ):
        self.llm = llm_provider
        self.memory = memory_provider
        self.system_prompt = system_prompt

    async def chat(self, user_message: str, session_id: Optional[str] = None) -> Result[Dict[str, Any]]:
        sid = session_id or str(uuid.uuid4())
        history = []
        if self.memory:
            await self.memory.add_message(sid, "user", user_message)
            history = await self.memory.get_messages(sid)

        res = await self.llm.generate_response(
            prompt=user_message,
            system_prompt=self.system_prompt,
            history=history
        )

        if res.is_success and self.memory:
            await self.memory.add_message(sid, "assistant", res.value.get("content", ""))

        return res

    async def stream_chat(self, user_message: str, session_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        sid = session_id or str(uuid.uuid4())
        if self.memory:
            await self.memory.add_message(sid, "user", user_message)

        async for chunk in self.llm.generate_stream(prompt=user_message, system_prompt=self.system_prompt):
            yield chunk
