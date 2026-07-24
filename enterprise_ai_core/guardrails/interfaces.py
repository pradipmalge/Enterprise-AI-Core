from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .models import GuardrailContext, GuardrailResult, GuardrailPhase

class IGuardrail(ABC):
    """Base interface for all Guardrail components."""
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def phase(self) -> GuardrailPhase:
        pass

class IPreRequestGuardrail(IGuardrail):
    """Evaluated on raw incoming user query before context engine processing."""
    @property
    def phase(self) -> GuardrailPhase:
        return GuardrailPhase.PRE_REQUEST

    @abstractmethod
    async def validate_request(self, user_query: str, ctx: GuardrailContext) -> GuardrailResult:
        pass

class IPrePromptGuardrail(IGuardrail):
    """Evaluated on full context envelope rendered prompt before LLM dispatch."""
    @property
    def phase(self) -> GuardrailPhase:
        return GuardrailPhase.PRE_PROMPT

    @abstractmethod
    async def validate_prompt(self, prompt: str, ctx: GuardrailContext) -> GuardrailResult:
        pass

class IPostPromptGuardrail(IGuardrail):
    """Evaluated on LLM output response before tool execution or final synthesis."""
    @property
    def phase(self) -> GuardrailPhase:
        return GuardrailPhase.POST_PROMPT

    @abstractmethod
    async def validate_llm_response(self, response_text: str, ctx: GuardrailContext) -> GuardrailResult:
        pass

class IPreToolGuardrail(IGuardrail):
    """Evaluated before executing a tool request (authorization, parameter safety)."""
    @property
    def phase(self) -> GuardrailPhase:
        return GuardrailPhase.PRE_TOOL

    @abstractmethod
    async def validate_tool_call(self, tool_name: str, tool_args: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        pass

class IPostToolGuardrail(IGuardrail):
    """Evaluated on tool execution result before returning observation to LLM context."""
    @property
    def phase(self) -> GuardrailPhase:
        return GuardrailPhase.POST_TOOL

    @abstractmethod
    async def validate_tool_result(self, tool_name: str, result: Any, ctx: GuardrailContext) -> GuardrailResult:
        pass

class IPostResponseGuardrail(IGuardrail):
    """Evaluated on finalized response before returning to end-user."""
    @property
    def phase(self) -> GuardrailPhase:
        return GuardrailPhase.POST_RESPONSE

    @abstractmethod
    async def validate_final_response(self, response_payload: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        pass
