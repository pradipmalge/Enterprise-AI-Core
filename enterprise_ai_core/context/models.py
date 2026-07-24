from enum import IntEnum
from typing import Dict, Any, List, Optional, Union

class ContextPriority(IntEnum):
    SYSTEM_PROMPT = 1
    SAFETY_RULES = 2
    DEVELOPER_INSTRUCTIONS = 3
    CURRENT_USER_REQUEST = 4
    CONVERSATION_HISTORY = 5
    RETRIEVED_KNOWLEDGE = 6  # RAG
    MEMORY = 7
    TOOL_RESULTS = 8
    METADATA = 9

class ContextFragment:
    """Represents a single modular piece of context injected by a provider."""
    def __init__(
        self,
        name: str,
        content: str,
        priority: ContextPriority = ContextPriority.METADATA,
        source: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        tokens_estimated: Optional[int] = None
    ):
        self.name = name
        self.content = content
        self.priority = priority
        self.source = source
        self.metadata = metadata or {}
        self.tokens_estimated = tokens_estimated or self._estimate_tokens(content)

    def _estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)

    def __repr__(self):
        return f"<ContextFragment name={self.name} priority={self.priority.name} tokens={self.tokens_estimated}>"

class ContextEnvelope:
    """Complete aggregated context package sent to LLM rendering."""
    def __init__(self, request_id: str, max_token_budget: int = 4096):
        self.request_id = request_id
        self.max_token_budget = max_token_budget
        self.fragments: List[ContextFragment] = []
        self.system_prompt: str = ""
        self.user_prompt: str = ""
        self.rendered_prompt: str = ""
        self.total_tokens: int = 0
        self.dropped_fragments: List[str] = []
        self.compressed: bool = False
        self.metadata: Dict[str, Any] = {}

    def add_fragment(self, fragment: ContextFragment):
        self.fragments.append(fragment)

    def sort_by_priority(self):
        self.fragments.sort(key=lambda f: f.priority.value)

    def calculate_total_tokens(self) -> int:
        self.total_tokens = sum(f.tokens_estimated for f in self.fragments)
        return self.total_tokens
