import logging
import uuid
import time
from typing import Dict, Any, List, Optional, Union
from .models import (
    GuardrailContext,
    GuardrailResult,
    GuardrailAction,
    GuardrailPhase,
    GuardrailPolicy,
    GuardrailConfiguration,
    ViolationReport
)
from .interfaces import (
    IGuardrail,
    IPreRequestGuardrail,
    IPrePromptGuardrail,
    IPostPromptGuardrail,
    IPreToolGuardrail,
    IPostToolGuardrail,
    IPostResponseGuardrail
)
from .builtins import (
    PromptInjectionGuardrail,
    JailbreakGuardrail,
    PIIGuardrail,
    SecretsGuardrail,
    ToolPermissionGuardrail,
    RateLimitGuardrail,
    TokenBudgetGuardrail,
    ContentModerationGuardrail,
    JSONSchemaValidationGuardrail,
    HallucinationDetectionGuardrail
)

logger = logging.getLogger("EnterpriseGuardrailsEngine")

class GuardrailRegistry:
    """Registry maintaining active guardrail instances grouped by phase and name."""

    def __init__(self):
        self._guardrails_by_name: Dict[str, IGuardrail] = {}
        self._guardrails_by_phase: Dict[GuardrailPhase, List[IGuardrail]] = {
            phase: [] for phase in GuardrailPhase
        }

    def register(self, guardrail: IGuardrail):
        self._guardrails_by_name[guardrail.name] = guardrail
        phase = guardrail.phase
        if guardrail not in self._guardrails_by_phase[phase]:
            self._guardrails_by_phase[phase].append(guardrail)
        logger.info(f"Registered Guardrail '{guardrail.name}' for phase [{phase.value}]")

    def unregister(self, name: str):
        if name in self._guardrails_by_name:
            g = self._guardrails_by_name.pop(name)
            if g in self._guardrails_by_phase[g.phase]:
                self._guardrails_by_phase[g.phase].remove(g)

    def get_guardrails(self, phase: GuardrailPhase) -> List[IGuardrail]:
        return self._guardrails_by_phase.get(phase, [])

    def get_by_name(self, name: str) -> Optional[IGuardrail]:
        return self._guardrails_by_name.get(name)


class GuardrailExecutor:
    """Executes guardrails sequentially or in parallel for a given phase."""

    def __init__(self, registry: GuardrailRegistry, config: GuardrailConfiguration):
        self.registry = registry
        self.config = config

    async def execute_phase(
        self,
        phase: GuardrailPhase,
        input_data: Any,
        ctx: GuardrailContext,
        extra_args: Optional[Dict[str, Any]] = None
    ) -> GuardrailResult:
        guardrails = self.registry.get_guardrails(phase)
        current_data = input_data
        extra_args = extra_args or {}

        for g in guardrails:
            res: GuardrailResult = GuardrailResult.allow()

            try:
                if phase == GuardrailPhase.PRE_REQUEST and isinstance(g, IPreRequestGuardrail):
                    res = await g.validate_request(current_data, ctx)
                elif phase == GuardrailPhase.PRE_PROMPT and isinstance(g, IPrePromptGuardrail):
                    res = await g.validate_prompt(current_data, ctx)
                elif phase == GuardrailPhase.POST_PROMPT and isinstance(g, IPostPromptGuardrail):
                    res = await g.validate_llm_response(current_data, ctx)
                elif phase == GuardrailPhase.PRE_TOOL and isinstance(g, IPreToolGuardrail):
                    tool_name = extra_args.get("tool_name", "")
                    tool_args = extra_args.get("tool_args", {})
                    res = await g.validate_tool_call(tool_name, tool_args, ctx)
                elif phase == GuardrailPhase.POST_TOOL and isinstance(g, IPostToolGuardrail):
                    tool_name = extra_args.get("tool_name", "")
                    res = await g.validate_tool_result(tool_name, current_data, ctx)
                elif phase == GuardrailPhase.POST_RESPONSE and isinstance(g, IPostResponseGuardrail):
                    res = await g.validate_final_response(current_data, ctx)

            except Exception as ex:
                logger.error(f"Error executing guardrail '{g.name}' in phase {phase.value}: {str(ex)}")
                viol = ViolationReport(
                    guardrail_name=g.name,
                    phase=phase,
                    message=f"Execution error in guardrail: {str(ex)}",
                    severity="HIGH"
                )
                res = GuardrailResult(action=GuardrailAction.BLOCK, violation=viol)

            # Handle Result Actions
            if res.violation:
                ctx.violations.append(res.violation)
                ctx.log_event("GUARDRAIL_VIOLATION", res.violation.to_dict())

            if res.action == GuardrailAction.BLOCK:
                ctx.log_event("GUARDRAIL_BLOCKED", {
                    "guardrail": g.name,
                    "phase": phase.value,
                    "message": res.violation.message if res.violation else "Blocked by policy"
                })
                if self.config.fail_fast:
                    return res

            elif res.action == GuardrailAction.MODIFY:
                current_data = res.modified_content
                ctx.log_event("GUARDRAIL_MODIFIED", {
                    "guardrail": g.name,
                    "phase": phase.value,
                    "info": res.metadata.get("info", "Content modified")
                })

            elif res.action == GuardrailAction.WARN:
                ctx.log_event("GUARDRAIL_WARNING", {
                    "guardrail": g.name,
                    "phase": phase.value,
                    "message": res.violation.message if res.violation else "Warning issued"
                })

        return GuardrailResult(action=GuardrailAction.ALLOW, modified_content=current_data)


class GuardrailPipeline:
    """Represents the ordered 6-stage lifecycle pipeline."""

    STAGES = [
        GuardrailPhase.PRE_REQUEST,
        GuardrailPhase.PRE_PROMPT,
        GuardrailPhase.POST_PROMPT,
        GuardrailPhase.PRE_TOOL,
        GuardrailPhase.POST_TOOL,
        GuardrailPhase.POST_RESPONSE
    ]


class GuardrailsEngine:
    """Primary Enterprise Guardrails Engine orchestrating safety, policies, and auditing."""

    def __init__(self, config: Optional[GuardrailConfiguration] = None):
        self.config = config or GuardrailConfiguration()
        self.registry = GuardrailRegistry()
        self.executor = GuardrailExecutor(self.registry, self.config)
        self.audit_log_store: List[Dict[str, Any]] = []

        # Auto-register standard built-in guardrails based on policy
        self._register_default_guardrails()

    def _register_default_guardrails(self):
        policy = self.config.policy

        if policy.enable_prompt_injection_check:
            self.registry.register(PromptInjectionGuardrail())
            self.registry.register(JailbreakGuardrail())

        if policy.enable_pii_redaction:
            self.registry.register(PIIGuardrail())

        if policy.enable_secrets_detection:
            self.registry.register(SecretsGuardrail())

        self.registry.register(ToolPermissionGuardrail(policy=policy))
        self.registry.register(RateLimitGuardrail(max_requests_per_minute=120))
        self.registry.register(TokenBudgetGuardrail(max_prompt_tokens=policy.max_prompt_tokens))
        self.registry.register(ContentModerationGuardrail())
        self.registry.register(JSONSchemaValidationGuardrail())
        self.registry.register(HallucinationDetectionGuardrail())

    def register_guardrail(self, guardrail: IGuardrail):
        """Allows registering custom or domain-specific guardrail implementations."""
        self.registry.register(guardrail)

    def create_context(self, request_id: Optional[str] = None, agent_id: str = "agent-core", user_role: str = "user") -> GuardrailContext:
        req_id = request_id or f"req-grd-{uuid.uuid4().hex[:6]}"
        return GuardrailContext(request_id=req_id, agent_id=agent_id, user_role=user_role)

    async def run_pre_request(self, user_query: str, ctx: GuardrailContext) -> GuardrailResult:
        """Stage 1: Pre-Request Validation & Filtering"""
        return await self.executor.execute_phase(GuardrailPhase.PRE_REQUEST, user_query, ctx)

    async def run_pre_prompt(self, rendered_prompt: str, ctx: GuardrailContext) -> GuardrailResult:
        """Stage 2: Pre-Prompt Validation & Policy Enforcement"""
        ctx.state["rendered_prompt"] = rendered_prompt
        return await self.executor.execute_phase(GuardrailPhase.PRE_PROMPT, rendered_prompt, ctx)

    async def run_post_prompt(self, llm_response_text: str, ctx: GuardrailContext) -> GuardrailResult:
        """Stage 3: Post-Prompt / LLM Output Validation"""
        return await self.executor.execute_phase(GuardrailPhase.POST_PROMPT, llm_response_text, ctx)

    async def run_pre_tool(self, tool_name: str, tool_args: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        """Stage 4: Pre-Tool Execution Authorization & Parameter Validation"""
        return await self.executor.execute_phase(
            GuardrailPhase.PRE_TOOL,
            input_data=tool_name,
            ctx=ctx,
            extra_args={"tool_name": tool_name, "tool_args": tool_args}
        )

    async def run_post_tool(self, tool_name: str, tool_result: Any, ctx: GuardrailContext) -> GuardrailResult:
        """Stage 5: Post-Tool Result Inspection & Verification"""
        return await self.executor.execute_phase(
            GuardrailPhase.POST_TOOL,
            input_data=tool_result,
            ctx=ctx,
            extra_args={"tool_name": tool_name}
        )

    async def run_post_response(self, response_payload: Dict[str, Any], ctx: GuardrailContext) -> GuardrailResult:
        """Stage 6: Final Response Safeguards & PII Output Scrubbing"""
        res = await self.executor.execute_phase(GuardrailPhase.POST_RESPONSE, response_payload, ctx)
        if self.config.auditing_enabled:
            self._audit_request(ctx)
        return res

    def _audit_request(self, ctx: GuardrailContext):
        record = {
            "request_id": ctx.request_id,
            "agent_id": ctx.agent_id,
            "user_role": ctx.user_role,
            "timestamp": time.time(),
            "violations": [v.to_dict() for v in ctx.violations],
            "audit_logs": ctx.audit_logs
        }
        self.audit_log_store.append(record)
        logger.info(f"[GuardrailsAudit] Logged audit record for request {ctx.request_id} with {len(ctx.violations)} violations.")
