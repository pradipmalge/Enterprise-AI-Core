import uuid
import time
from typing import Dict, Any, List, Optional
from enterprise_ai_core.agent.state import AgentState, AgentStep
from enterprise_ai_core.agent.planner import ExecutionPlanner
from enterprise_ai_core.llm.interfaces import ILLMProvider
from enterprise_ai_core.tools.registry import ToolRegistry
from enterprise_ai_core.memory.interfaces import IMemoryProvider
from enterprise_ai_core.cache.interfaces import ICache
from enterprise_ai_core.messaging.interfaces import IMessageBus
from enterprise_ai_core.mcp.client import MCPClient
from enterprise_ai_core.common.result import Result
from enterprise_ai_core.guardrails import (
    GuardrailsEngine,
    GuardrailAction,
    GuardrailContext,
    GuardrailPolicy
)

class EnterpriseAgent:
    def __init__(
        self,
        llm_provider: ILLMProvider,
        tool_registry: ToolRegistry,
        memory_provider: Optional[IMemoryProvider] = None,
        cache_provider: Optional[ICache] = None,
        message_bus: Optional[IMessageBus] = None,
        mcp_clients: Optional[List[MCPClient]] = None,
        system_prompt: str = "You are an Enterprise AI Agent operating under Clean Architecture.",
        context_engine: Optional[Any] = None,
        guardrails_engine: Optional[GuardrailsEngine] = None
    ):
        self.agent_id = f"agent-{uuid.uuid4().hex[:6]}"
        self.llm = llm_provider
        self.tools = tool_registry
        self.memory = memory_provider
        self.cache = cache_provider
        self.bus = message_bus
        self.mcp_clients = mcp_clients or []
        self.system_prompt = system_prompt
        self.planner = ExecutionPlanner(self.tools)
        self.guardrails = guardrails_engine or GuardrailsEngine()
        
        if context_engine is None:
            from enterprise_ai_core.context import ContextEngine, SystemContextProvider
            self.context_engine = ContextEngine()
            self.context_engine.register_provider(SystemContextProvider(self.system_prompt))
        else:
            self.context_engine = context_engine

    def register_guardrail(self, guardrail: Any):
        self.guardrails.register_guardrail(guardrail)

    @classmethod
    def builder(cls) -> 'AgentBuilder':
        from enterprise_ai_core.agent.builder import AgentBuilder
        return AgentBuilder()

    async def chat(self, user_query: str, session_id: Optional[str] = None, user_role: str = "user") -> Result[Dict[str, Any]]:
        sid = session_id or f"sess-{uuid.uuid4().hex[:6]}"
        start_time = time.time()

        # Guardrails Stage 1: Pre-Request Validation
        grd_ctx = self.guardrails.create_context(agent_id=self.agent_id, user_role=user_role)
        pre_req_res = await self.guardrails.run_pre_request(user_query, grd_ctx)

        if pre_req_res.action == GuardrailAction.BLOCK:
            return Result.ok({
                "response": f"Request blocked by Enterprise Guardrail policy: {pre_req_res.violation.message if pre_req_res.violation else 'Policy violation'}",
                "agent_id": self.agent_id,
                "session_id": sid,
                "status": "BLOCKED_BY_GUARDRAIL",
                "execution_time_ms": round((time.time() - start_time) * 1000, 2),
                "guardrail_violations": [v.to_dict() for v in grd_ctx.violations]
            })

        if pre_req_res.modified_content:
            user_query = pre_req_res.modified_content

        # Build Context via ContextEngine before execution
        history_msgs = []
        if self.memory:
            history_res = await self.memory.get_messages(sid)
            if hasattr(history_res, "is_success"):
                if history_res.is_success:
                    history_msgs = history_res.value
            elif isinstance(history_res, list):
                history_msgs = history_res

        tools_list = []
        for name, tool_inst in self.tools._tools.items():
            desc = ""
            if hasattr(tool_inst, "metadata") and hasattr(tool_inst.metadata, "description"):
                desc = tool_inst.metadata.description
            elif hasattr(tool_inst, "description"):
                desc = getattr(tool_inst, "description", "")
            tools_list.append({"name": name, "description": desc or f"Tool {name}"})

        context_payload = {
            "agent_id": self.agent_id,
            "session_id": sid,
            "user_query": user_query,
            "system_prompt": self.system_prompt,
            "conversation_history": history_msgs,
            "available_tools": tools_list
        }

        context_envelope = await self.context_engine.build_context(context_payload)

        # Guardrails Stage 2: Pre-Prompt Validation
        rendered_prompt = (context_envelope.system_prompt or "") + "\n" + (context_envelope.user_prompt or "")
        pre_prompt_res = await self.guardrails.run_pre_prompt(rendered_prompt, grd_ctx)

        if pre_prompt_res.action == GuardrailAction.BLOCK:
            return Result.ok({
                "response": f"Prompt blocked by Enterprise Guardrail policy: {pre_prompt_res.violation.message if pre_prompt_res.violation else 'Policy violation'}",
                "agent_id": self.agent_id,
                "session_id": sid,
                "status": "BLOCKED_BY_GUARDRAIL",
                "execution_time_ms": round((time.time() - start_time) * 1000, 2),
                "guardrail_violations": [v.to_dict() for v in grd_ctx.violations]
            })

        # Check cache
        if self.cache:
            cached_res = await self.cache.get(f"agent:query:{user_query}")
            if cached_res:
                return Result.ok({
                    "response": cached_res,
                    "agent_id": self.agent_id,
                    "session_id": sid,
                    "execution_time_ms": round((time.time() - start_time) * 1000, 2),
                    "cached": True,
                    "steps": [],
                    "context_summary": {
                        "total_tokens": context_envelope.total_tokens,
                        "fragments": [f.name for f in context_envelope.fragments]
                    }
                })

        # Memory store query
        if self.memory:
            await self.memory.add_message(sid, "user", user_query)

        # Plan execution
        state = AgentState(agent_id=self.agent_id, user_query=user_query, status="PLANNING")
        steps = self.planner.create_plan(user_query)
        state.steps = steps

        # Execute steps
        trace_logs = [
            f"[GuardrailsEngine] Active context initialized (Request ID: {grd_ctx.request_id}).",
            f"[ContextEngine] Built context envelope with {len(context_envelope.fragments)} fragments ({context_envelope.total_tokens} tokens)."
        ]
        final_answer = ""

        for step in steps:
            state.status = "EXECUTING"
            if step.action_tool:
                # Guardrails Stage 4: Pre-Tool Authorization
                pre_tool_res = await self.guardrails.run_pre_tool(step.action_tool, step.action_args, grd_ctx)
                if pre_tool_res.action == GuardrailAction.BLOCK:
                    step.observation = f"Tool execution blocked by policy: {pre_tool_res.violation.message if pre_tool_res.violation else 'Access denied'}"
                    trace_logs.append(f"[Guardrail Block] Tool '{step.action_tool}' blocked: {step.observation}")
                    continue

                trace_logs.append(f"[Step {step.step_number}] Executing tool '{step.action_tool}'...")
                res = await self.tools.execute_tool(step.action_tool, **step.action_args)
                
                if res.is_success:
                    # Guardrails Stage 5: Post-Tool Inspection
                    post_tool_res = await self.guardrails.run_post_tool(step.action_tool, res.value, grd_ctx)
                    if post_tool_res.action == GuardrailAction.BLOCK:
                        step.observation = f"Tool result blocked by Guardrail: {post_tool_res.violation.message if post_tool_res.violation else 'Insecure result'}"
                    else:
                        step.observation = str(post_tool_res.modified_content if post_tool_res.modified_content is not None else res.value)
                        step.completed = True
                        trace_logs.append(f"[Observation] Tool output: {step.observation}")
                else:
                    step.observation = f"Error: {res.error}"
                    trace_logs.append(f"[Tool Error] {res.error}")
            else:
                # LLM Direct reasoning call using Context Engine prompts
                llm_res = await self.llm.generate_response(
                    prompt=context_envelope.user_prompt or user_query,
                    system_prompt=context_envelope.system_prompt or self.system_prompt
                )
                if llm_res.is_success:
                    final_answer = llm_res.value.get("content", "")
                    step.completed = True
                else:
                    final_answer = f"Agent processing completed for '{user_query}'."

        if not final_answer:
            obs = [s.observation for s in steps if s.observation]
            if obs:
                final_answer = f"Completed agent loop. Summary of findings: {'; '.join(obs)}"
            else:
                final_answer = f"Processed enterprise request for: '{user_query}'."

        # Guardrails Stage 3: Post-Prompt LLM Validation
        post_prompt_res = await self.guardrails.run_post_prompt(final_answer, grd_ctx)
        if post_prompt_res.action == GuardrailAction.BLOCK:
            final_answer = f"Response generation blocked by policy: {post_prompt_res.violation.message if post_prompt_res.violation else 'Invalid output'}"
        elif post_prompt_res.modified_content:
            final_answer = post_prompt_res.modified_content

        state.status = "SUCCESS"
        state.final_answer = final_answer

        # Publish event
        if self.bus:
            await self.bus.publish("agent.completed", {
                "agent_id": self.agent_id,
                "session_id": sid,
                "query": user_query,
                "final_answer": final_answer
            })

        # Cache answer
        if self.cache:
            await self.cache.set(f"agent:query:{user_query}", final_answer, ttl=300)

        # Save to memory
        if self.memory:
            await self.memory.add_message(sid, "assistant", final_answer)

        execution_time_ms = round((time.time() - start_time) * 1000, 2)

        response_payload = {
            "response": final_answer,
            "agent_id": self.agent_id,
            "session_id": sid,
            "status": "SUCCESS",
            "execution_time_ms": execution_time_ms,
            "steps": [
                {
                    "step_number": s.step_number,
                    "thought": s.thought,
                    "action_tool": s.action_tool,
                    "observation": s.observation
                } for s in steps
            ],
            "trace_logs": trace_logs,
            "context_summary": {
                "request_id": context_envelope.request_id,
                "total_tokens": context_envelope.total_tokens,
                "fragments": [f.name for f in context_envelope.fragments],
                "dropped": context_envelope.dropped_fragments,
                "compressed": context_envelope.compressed
            }
        }

        # Guardrails Stage 6: Post-Response Validation & Scrubbing
        post_resp_res = await self.guardrails.run_post_response(response_payload, grd_ctx)
        if post_resp_res.modified_content and isinstance(post_resp_res.modified_content, dict):
            response_payload = post_resp_res.modified_content

        response_payload["guardrail_summary"] = {
            "request_id": grd_ctx.request_id,
            "violations_count": len(grd_ctx.violations),
            "violations": [v.to_dict() for v in grd_ctx.violations],
            "audit_logs_count": len(grd_ctx.audit_logs)
        }

        return Result.ok(response_payload)
