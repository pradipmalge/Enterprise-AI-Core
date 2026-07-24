from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import uuid
import time

@dataclass
class RequestContext:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    user_id: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    correlation_id: str = field(default_factory=lambda: f"corr-{uuid.uuid4().hex[:8]}")
    timestamp: float = field(default_factory=time.time)

@dataclass
class ConversationContext:
    session_id: str = field(default_factory=lambda: f"sess-{uuid.uuid4().hex[:8]}")
    user_id: str = "anonymous"
    metadata: Dict[str, Any] = field(default_factory=dict)
    system_prompt: str = "You are a helpful enterprise AI assistant."
    turn_count: int = 0

@dataclass
class ResponseContext:
    request_id: str
    status: str = "success"
    latency_ms: float = 0.0
    tokens_used: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    model: str = "default-model"

@dataclass
class ExecutionContext:
    request_context: RequestContext = field(default_factory=RequestContext)
    conversation_context: ConversationContext = field(default_factory=ConversationContext)
    variables: Dict[str, Any] = field(default_factory=dict)
    step_history: List[Dict[str, Any]] = field(default_factory=list)

    def set_variable(self, key: str, value: Any):
        self.variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)
