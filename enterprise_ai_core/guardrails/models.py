import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional, Union

class GuardrailAction(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    MODIFY = "MODIFY"
    WARN = "WARN"

class GuardrailPhase(str, Enum):
    PRE_REQUEST = "PRE_REQUEST"
    PRE_PROMPT = "PRE_PROMPT"
    POST_PROMPT = "POST_PROMPT"
    PRE_TOOL = "PRE_TOOL"
    POST_TOOL = "POST_TOOL"
    POST_RESPONSE = "POST_RESPONSE"

class ViolationReport:
    """Represents a policy or security violation detected by a guardrail."""
    def __init__(
        self,
        guardrail_name: str,
        phase: GuardrailPhase,
        message: str,
        severity: str = "HIGH", # CRITICAL, HIGH, MEDIUM, LOW
        details: Optional[Dict[str, Any]] = None
    ):
        self.id = f"viol-{uuid.uuid4().hex[:6]}"
        self.guardrail_name = guardrail_name
        self.phase = phase
        self.message = message
        self.severity = severity
        self.details = details or {}
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "guardrail_name": self.guardrail_name,
            "phase": self.phase.value if isinstance(self.phase, GuardrailPhase) else str(self.phase),
            "message": self.message,
            "severity": self.severity,
            "details": self.details,
            "timestamp": self.timestamp
        }

class GuardrailResult:
    """Result returned by a guardrail evaluation."""
    def __init__(
        self,
        action: GuardrailAction = GuardrailAction.ALLOW,
        modified_content: Optional[Any] = None,
        violation: Optional[ViolationReport] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.action = action
        self.modified_content = modified_content
        self.violation = violation
        self.metadata = metadata or {}

    @classmethod
    def allow(cls, modified_content: Optional[Any] = None) -> 'GuardrailResult':
        return cls(action=GuardrailAction.ALLOW, modified_content=modified_content)

    @classmethod
    def block(cls, guardrail_name: str, phase: GuardrailPhase, message: str, details: Optional[Dict[str, Any]] = None) -> 'GuardrailResult':
        viol = ViolationReport(guardrail_name=guardrail_name, phase=phase, message=message, severity="CRITICAL", details=details)
        return cls(action=GuardrailAction.BLOCK, violation=viol)

    @classmethod
    def modify(cls, modified_content: Any, message: str = "Content modified by policy") -> 'GuardrailResult':
        return cls(action=GuardrailAction.MODIFY, modified_content=modified_content, metadata={"info": message})

    @classmethod
    def warn(cls, guardrail_name: str, phase: GuardrailPhase, message: str) -> 'GuardrailResult':
        viol = ViolationReport(guardrail_name=guardrail_name, phase=phase, message=message, severity="LOW")
        return cls(action=GuardrailAction.WARN, violation=viol)

class GuardrailContext:
    """Holds state passed across guardrail pipeline stages."""
    def __init__(self, request_id: str, agent_id: str = "agent-core", user_role: str = "user"):
        self.request_id = request_id
        self.agent_id = agent_id
        self.user_role = user_role
        self.state: Dict[str, Any] = {}
        self.audit_logs: List[Dict[str, Any]] = []
        self.violations: List[ViolationReport] = []

    def log_event(self, event: str, payload: Dict[str, Any]):
        self.audit_logs.append({
            "timestamp": time.time(),
            "event": event,
            "payload": payload
        })

class GuardrailPolicy:
    """Declarative policy configuration for Guardrails Engine."""
    def __init__(
        self,
        allow_tools: Optional[List[str]] = None,
        deny_tools: Optional[List[str]] = None,
        max_prompt_tokens: int = 8000,
        max_response_tokens: int = 2000,
        allowed_roles: Optional[List[str]] = None,
        enable_pii_redaction: bool = True,
        enable_prompt_injection_check: bool = True,
        enable_secrets_detection: bool = True,
        custom_rules: Optional[Dict[str, Any]] = None
    ):
        self.allow_tools = allow_tools
        self.deny_tools = deny_tools or []
        self.max_prompt_tokens = max_prompt_tokens
        self.max_response_tokens = max_response_tokens
        self.allowed_roles = allowed_roles
        self.enable_pii_redaction = enable_pii_redaction
        self.enable_prompt_injection_check = enable_prompt_injection_check
        self.enable_secrets_detection = enable_secrets_detection
        self.custom_rules = custom_rules or {}

class GuardrailConfiguration:
    """Global configuration wrapper for Guardrails Engine."""
    def __init__(
        self,
        policy: Optional[GuardrailPolicy] = None,
        fail_fast: bool = True,
        auditing_enabled: bool = True
    ):
        self.policy = policy or GuardrailPolicy()
        self.fail_fast = fail_fast
        self.auditing_enabled = auditing_enabled
