from typing import List, Dict, Any, Optional
from enterprise_ai_core.memory.interfaces import IMemoryProvider

class ConversationMemory(IMemoryProvider):
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self._sessions: Dict[str, List[Dict[str, Any]]] = {}

    async def add_message(self, session_id: str, role: str, content: str) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append({"role": role, "content": content})
        if len(self._sessions[session_id]) > self.window_size * 2:
            self._sessions[session_id] = self._sessions[session_id][-self.window_size * 2:]

    async def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        msgs = self._sessions.get(session_id, [])
        if limit:
            return msgs[-limit:]
        return msgs.copy()

    async def clear(self, session_id: str) -> None:
        if session_id in self._sessions:
            self._sessions[session_id] = []
