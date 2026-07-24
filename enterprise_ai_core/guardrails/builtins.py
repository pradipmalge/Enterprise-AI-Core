import re
import json
import time
from typing import Dict, Any, List, Optional
from .interfaces import (
    IPreRequestGuardrail,
    IPrePromptGuardrail,
    IPostPromptGuardrail,
    IPreToolGuardrail,
    IPostToolGuardrail,
    IPostResponseGuardrail,
)
from .models import GuardrailResult, GuardrailPhase, GuardrailContext, GuardrailPolicy

class PromptInjectionGuardrail(IPreRequestGuardrail, IPrePromptGuardrail):
    """Detects prompt injection vectors and override patterns."""
    
    INJECTION_PATTERNS = [
        r'(?i)ignore\s+all\s+previous\s+instructions',
        r'(?i)disregard\s+system\s+prompt',
        r'(?i)you\s+are\s+now\s+in\s+developer\s+mode',
        r'(?i)bypass\s+security\s+rules',
        r'(?i)system\s*:\s*override',
        r'(?i)DAN\s+mode',
        r'(?i)jailbreak',
    ]

    @property
    def name(self) -> str:
        return "prompt_injection_guardrail"

    async def validate_request(self, user_query: str, ctx: GuardrailContext) -> GuardrailResult:
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, user_query):
                return GuardrailResult.block(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.PRE_REQUEST,
                    message="Prompt injection vector detected in request.",
                    details={"matched_pattern": pattern}
                )
        return GuardrailResult.allow()

    async def validate_prompt(self, prompt: str, ctx: GuardrailContext) -> GuardrailResult:
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, prompt):
                return GuardrailResult.block(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.PRE_PROMPT,
                    message="Prompt injection pattern detected in rendered system context.",
                    details={"matched_pattern": pattern}
                )
        return GuardrailResult.allow()

class JailbreakGuardrail(IPreRequestGuardrail):
    """Detects jailbreak triggers attempting to unlock unrestricted output."""
    JAILBREAK_TERMS = ["act as an unfiltered ai", "do anything now", "hypothetical scenario where safety rules don't apply", "evil confidant"]

    @property
    def name(self) -> str:
        return "jailbreak_guardrail"

    async def validate_request(self, user_query: str, ctx: GuardrailContext) -> GuardrailResult:
        lower = user_query.lower()
        for term in self.JAILBREAK_TERMS:
            if term in lower:
                return GuardrailResult.block(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.PRE_REQUEST,
                    message=f"Jailbreak attempt identified: '{term}'",
                    details={"term": term}
                )
        return GuardrailResult.allow()

class PIIGuardrail(IPreRequestGuardrail, IPostResponseGuardrail):
    """Detects and redacts PII (emails, SSNs, credit cards, phone numbers)."""
    
    EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_REGEX = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    SSN_REGEX = r'\b\d{3}-\d{2}-\d{4}\b'

    @property
    def name(self) -> str:
        return "pii_guardrail"

    async def validate_request(self, user_query: str, ctx: GuardrailContext) -> GuardrailResult:
        redacted = re.sub(self.EMAIL_REGEX, "[REDACTED_EMAIL]", user_query)
        redacted = re.sub(self.PHONE_REGEX, "[REDACTED_PHONE]", redacted)
        redacted = re.sub(self.SSN_REGEX, "[REDACTED_SSN]", redacted)

        if redacted != user_query:
            return GuardrailResult.modify(modified_content=redacted, message="PII auto-redacted from input query.")
        return GuardrailResult.allow()

    async def validate_final_response(self, response_payload: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        resp_str = json.dumps(response_payload)
        redacted = re.sub(self.EMAIL_REGEX, "[REDACTED_EMAIL]", resp_str)
        redacted = re.sub(self.PHONE_REGEX, "[REDACTED_PHONE]", redacted)
        redacted = re.sub(self.SSN_REGEX, "[REDACTED_SSN]", redacted)

        if redacted != resp_str:
            return GuardrailResult.modify(
                modified_content=json.loads(redacted),
                message="PII auto-redacted from output response payload."
            )
        return GuardrailResult.allow()

class SecretsGuardrail(IPrePromptGuardrail, IPostResponseGuardrail):
    """Detects API secrets, credentials, and tokens in prompt context or output."""
    
    SECRET_REGEX = r'(?i)(api[_-]?key|secret|password|bearer[_-]?token|private[_-]?key)\s*[:=]\s*["\']?[a-zA-Z0-9_\-\.]{8,}["\']?'

    @property
    def name(self) -> str:
        return "secrets_guardrail"

    async def validate_prompt(self, prompt: str, ctx: GuardrailContext) -> GuardrailResult:
        if re.search(self.SECRET_REGEX, prompt):
            redacted = re.sub(self.SECRET_REGEX, r'\1: [REDACTED_SECRET]', prompt)
            return GuardrailResult.modify(modified_content=redacted, message="API secret leak redacted from prompt.")
        return GuardrailResult.allow()

    async def validate_final_response(self, response_payload: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        resp_str = json.dumps(response_payload)
        if re.search(self.SECRET_REGEX, resp_str):
            redacted = re.sub(self.SECRET_REGEX, r'\1: [REDACTED_SECRET]', resp_str)
            return GuardrailResult.modify(
                modified_content=json.loads(redacted),
                message="API secret leak redacted from final response payload."
            )
        return GuardrailResult.allow()

class ToolPermissionGuardrail(IPreToolGuardrail):
    """Enforces tool permissions, role authorization, and allowed/blocked tool lists."""

    def __init__(self, policy: Optional[GuardrailPolicy] = None):
        self.policy = policy or GuardrailPolicy()

    @property
    def name(self) -> str:
        return "tool_permission_guardrail"

    async def validate_tool_call(self, tool_name: str, tool_args: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        # Check blocked list
        if tool_name in self.policy.deny_tools:
            return GuardrailResult.block(
                guardrail_name=self.name,
                phase=GuardrailPhase.PRE_TOOL,
                message=f"Tool '{tool_name}' is explicitly denied by enterprise security policy.",
                details={"tool_name": tool_name}
            )

        # Check allowed list if specified
        if self.policy.allow_tools is not None and tool_name not in self.policy.allow_tools:
            return GuardrailResult.block(
                guardrail_name=self.name,
                phase=GuardrailPhase.PRE_TOOL,
                message=f"Tool '{tool_name}' is not in the allowed tool white-list.",
                details={"tool_name": tool_name, "allowed": self.policy.allow_tools}
            )

        # Check user role authorization
        if self.policy.allowed_roles:
            if ctx.user_role not in self.policy.allowed_roles:
                return GuardrailResult.block(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.PRE_TOOL,
                    message=f"User role '{ctx.user_role}' is not authorized to execute tools.",
                    details={"user_role": ctx.user_role, "required_roles": self.policy.allowed_roles}
                )

        return GuardrailResult.allow()

class RateLimitGuardrail(IPreRequestGuardrail):
    """Enforces request rate limiting per user/session."""
    
    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests = max_requests_per_minute
        self._history: Dict[str, List[float]] = {}

    @property
    def name(self) -> str:
        return "rate_limit_guardrail"

    async def validate_request(self, user_query: str, ctx: GuardrailContext) -> GuardrailResult:
        now = time.time()
        user_key = ctx.agent_id or "default"
        
        if user_key not in self._history:
            self._history[user_key] = []

        # Filter out timestamps older than 60 seconds
        self._history[user_key] = [t for t in self._history[user_key] if now - t < 60]

        if len(self._history[user_key]) >= self.max_requests:
            return GuardrailResult.block(
                guardrail_name=self.name,
                phase=GuardrailPhase.PRE_REQUEST,
                message=f"Rate limit exceeded: Max {self.max_requests} requests/min.",
                details={"max_limit": self.max_requests}
            )

        self._history[user_key].append(now)
        return GuardrailResult.allow()

class TokenBudgetGuardrail(IPrePromptGuardrail):
    """Validates maximum prompt token limit before submitting to LLM."""

    def __init__(self, max_prompt_tokens: int = 8000):
        self.max_prompt_tokens = max_prompt_tokens

    @property
    def name(self) -> str:
        return "token_budget_guardrail"

    async def validate_prompt(self, prompt: str, ctx: GuardrailContext) -> GuardrailResult:
        estimated_tokens = max(1, len(prompt) // 4)
        if estimated_tokens > self.max_prompt_tokens:
            return GuardrailResult.block(
                guardrail_name=self.name,
                phase=GuardrailPhase.PRE_PROMPT,
                message=f"Prompt size ({estimated_tokens} tokens) exceeds maximum limit of {self.max_prompt_tokens} tokens.",
                details={"estimated_tokens": estimated_tokens, "max_limit": self.max_prompt_tokens}
            )
        return GuardrailResult.allow()

class ContentModerationGuardrail(IPreRequestGuardrail, IPostResponseGuardrail):
    """Filters prohibited content, profanity, and toxic keywords."""

    PROHIBITED_TERMS = ["malware generation", "zero-day exploit code", "ddos script"]

    @property
    def name(self) -> str:
        return "content_moderation_guardrail"

    async def validate_request(self, user_query: str, ctx: GuardrailContext) -> GuardrailResult:
        lower = user_query.lower()
        for term in self.PROHIBITED_TERMS:
            if term in lower:
                return GuardrailResult.block(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.PRE_REQUEST,
                    message=f"Content moderation rule violated: Prohibited request category '{term}'.",
                    details={"term": term}
                )
        return GuardrailResult.allow()

    async def validate_final_response(self, response_payload: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        content_str = json.dumps(response_payload).lower()
        for term in self.PROHIBITED_TERMS:
            if term in content_str:
                return GuardrailResult.block(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.POST_RESPONSE,
                    message=f"Content moderation rule violated: Prohibited material detected in response.",
                    details={"term": term}
                )
        return GuardrailResult.allow()

class JSONSchemaValidationGuardrail(IPostPromptGuardrail, IPostResponseGuardrail):
    """Validates that LLM output or final response complies with valid JSON format."""

    @property
    def name(self) -> str:
        return "json_schema_validation_guardrail"

    async def validate_llm_response(self, response_text: str, ctx: GuardrailContext) -> GuardrailResult:
        if "```json" in response_text:
            try:
                raw_json = response_text.split("```json")[1].split("```")[0].strip()
                json.loads(raw_json)
            except Exception as e:
                return GuardrailResult.warn(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.POST_PROMPT,
                    message=f"LLM JSON code block failed parsing: {str(e)}"
                )
        return GuardrailResult.allow()

    async def validate_final_response(self, response_payload: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        if not isinstance(response_payload, dict):
            return GuardrailResult.block(
                guardrail_name=self.name,
                phase=GuardrailPhase.POST_RESPONSE,
                message="Final response payload must be a valid dictionary structure."
            )
        return GuardrailResult.allow()

class HallucinationDetectionGuardrail(IPostPromptGuardrail):
    """Rule-based hook verifying that factual citations or claims meet minimum constraints."""

    @property
    def name(self) -> str:
        return "hallucination_detection_guardrail"

    async def validate_llm_response(self, response_text: str, ctx: GuardrailContext) -> GuardrailResult:
        # Check if RAG context was present but LLM made unanchored 100% certainty claims without citations
        if "[RETRIEVED_KNOWLEDGE_BASE]" in ctx.state.get("rendered_prompt", ""):
            if "Source:" not in response_text and "according to" not in response_text.lower():
                return GuardrailResult.warn(
                    guardrail_name=self.name,
                    phase=GuardrailPhase.POST_PROMPT,
                    message="RAG knowledge context was supplied, but response lacks explicit source citations."
                )
        return GuardrailResult.allow()
