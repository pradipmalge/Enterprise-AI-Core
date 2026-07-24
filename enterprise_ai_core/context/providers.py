import json
from typing import Dict, Any, List, Optional, Callable
from .interfaces import IContextProvider
from .models import ContextFragment, ContextPriority

class SystemContextProvider(IContextProvider):
    def __init__(self, system_prompt: str = "You are an Enterprise AI Agent operating under Clean Architecture."):
        self._prompt = system_prompt

    @property
    def name(self) -> str:
        return "system"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        prompt = request.get("system_prompt", self._prompt)
        return [
            ContextFragment(
                name="system_prompt",
                content=f"[SYSTEM_INSTRUCTIONS]\n{prompt}",
                priority=ContextPriority.SYSTEM_PROMPT,
                source="SystemContextProvider"
            )
        ]

class DeveloperContextProvider(IContextProvider):
    def __init__(self, instructions: str = ""):
        self.instructions = instructions

    @property
    def name(self) -> str:
        return "developer"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        dev_inst = request.get("developer_instructions", self.instructions)
        if not dev_inst:
            return []
        return [
            ContextFragment(
                name="developer_instructions",
                content=f"[DEVELOPER_INSTRUCTIONS]\n{dev_inst}",
                priority=ContextPriority.DEVELOPER_INSTRUCTIONS,
                source="DeveloperContextProvider"
            )
        ]

class ConversationContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "conversation"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        history = request.get("conversation_history", [])
        if not history:
            return []

        formatted = []
        for msg in history:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")

        return [
            ContextFragment(
                name="conversation_history",
                content="[CONVERSATION_HISTORY]\n" + "\n".join(formatted),
                priority=ContextPriority.CONVERSATION_HISTORY,
                source="ConversationContextProvider"
            )
        ]

class UserContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "user"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        query = request.get("user_query", request.get("query", ""))
        if not query:
            return []
        return [
            ContextFragment(
                name="user_query",
                content=f"[CURRENT_USER_REQUEST]\n{query}",
                priority=ContextPriority.CURRENT_USER_REQUEST,
                source="UserContextProvider"
            )
        ]

class SessionContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "session"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        session_id = request.get("session_id", "default-session")
        session_meta = request.get("session_metadata", {})
        content = f"[SESSION_CONTEXT]\nSession ID: {session_id}\nMetadata: {json.dumps(session_meta)}"
        return [
            ContextFragment(
                name="session_context",
                content=content,
                priority=ContextPriority.METADATA,
                source="SessionContextProvider"
            )
        ]

class MemoryContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "memory"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        memories = request.get("memory_facts", [])
        if not memories:
            return []
        formatted = "\n".join(f"- {m}" for m in memories)
        return [
            ContextFragment(
                name="recalled_memory",
                content=f"[LONG_TERM_MEMORY_FACTS]\n{formatted}",
                priority=ContextPriority.MEMORY,
                source="MemoryContextProvider"
            )
        ]

class KnowledgeContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "knowledge"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        rag_chunks = request.get("rag_chunks", [])
        if not rag_chunks:
            return []
        formatted = []
        for idx, chunk in enumerate(rag_chunks, 1):
            src = chunk.get("source", f"Chunk #{idx}")
            txt = chunk.get("content", str(chunk))
            formatted.append(f"[{idx}] Source: {src}\n{txt}")
        
        return [
            ContextFragment(
                name="knowledge_base_rag",
                content="[RETRIEVED_KNOWLEDGE_BASE]\n" + "\n\n".join(formatted),
                priority=ContextPriority.RETRIEVED_KNOWLEDGE,
                source="KnowledgeContextProvider"
            )
        ]

class DocumentContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "document"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        docs = request.get("attached_documents", [])
        if not docs:
            return []
        formatted = []
        for doc in docs:
            name = doc.get("name", "Document")
            content = doc.get("content", "")
            formatted.append(f"--- Document: {name} ---\n{content}")

        return [
            ContextFragment(
                name="attached_documents",
                content="[ATTACHED_DOCUMENTS]\n" + "\n\n".join(formatted),
                priority=ContextPriority.RETRIEVED_KNOWLEDGE,
                source="DocumentContextProvider"
            )
        ]

class ToolContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "tool"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        tools = request.get("available_tools", [])
        tool_results = request.get("tool_results", [])
        fragments = []

        if tools:
            tool_descs = [f"- {t.get('name')}: {t.get('description')}" for t in tools]
            fragments.append(
                ContextFragment(
                    name="tool_definitions",
                    content="[AVAILABLE_TOOLS]\n" + "\n".join(tool_descs),
                    priority=ContextPriority.DEVELOPER_INSTRUCTIONS,
                    source="ToolContextProvider"
                )
            )

        if tool_results:
            results_str = "\n".join(f"- Tool '{r.get('tool')}': {r.get('output')}" for r in tool_results)
            fragments.append(
                ContextFragment(
                    name="tool_execution_results",
                    content="[TOOL_EXECUTION_RESULTS]\n" + results_str,
                    priority=ContextPriority.TOOL_RESULTS,
                    source="ToolContextProvider"
                )
            )

        return fragments

class AgentContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "agent"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        agent_id = request.get("agent_id", "agent-core")
        capabilities = request.get("capabilities", ["Clean Architecture", "Tool Calling", "RAG"])
        content = f"[AGENT_IDENTITY]\nAgent ID: {agent_id}\nCapabilities: {', '.join(capabilities)}"
        return [
            ContextFragment(
                name="agent_identity",
                content=content,
                priority=ContextPriority.SYSTEM_PROMPT,
                source="AgentContextProvider"
            )
        ]

class ExecutionContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "execution"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        state = request.get("execution_state", "IDLE")
        step = request.get("current_step", 1)
        content = f"[EXECUTION_STATE]\nState: {state}\nCurrent Step: {step}"
        return [
            ContextFragment(
                name="execution_state",
                content=content,
                priority=ContextPriority.METADATA,
                source="ExecutionContextProvider"
            )
        ]

class RequestContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "request"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        req_id = request.get("request_id", "req-001")
        timestamp = request.get("timestamp", "2026-07-23")
        content = f"[REQUEST_METADATA]\nRequest ID: {req_id}\nTimestamp: {timestamp}"
        return [
            ContextFragment(
                name="request_metadata",
                content=content,
                priority=ContextPriority.METADATA,
                source="RequestContextProvider"
            )
        ]

class ResponseContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "response"

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        format_req = request.get("response_format", "JSON / Markdown")
        content = f"[RESPONSE_FORMAT_REQUIREMENTS]\nExpected Output Format: {format_req}"
        return [
            ContextFragment(
                name="response_formatting",
                content=content,
                priority=ContextPriority.DEVELOPER_INSTRUCTIONS,
                source="ResponseContextProvider"
            )
        ]

class CustomContextProvider(IContextProvider):
    def __init__(self, provider_name: str, fn: Callable[[Dict[str, Any]], List[ContextFragment]]):
        self._name = provider_name
        self._fn = fn

    @property
    def name(self) -> str:
        return self._name

    async def provide_context(self, request: Dict[str, Any]) -> List[ContextFragment]:
        res = self._fn(request)
        return res if isinstance(res, list) else [res]
