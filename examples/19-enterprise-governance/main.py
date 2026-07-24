import asyncio
import json
from enterprise_ai_core import (
    EnterpriseAgent,
    ModelRoutingEngine,
    AIPolicyEngine,
    AIPolicy,
    GuardrailPolicy,
    FeatureFlagsManager,
    EnvironmentProfileManager,
    EnvironmentType,
    FrameworkPlugin,
    PluginValidator,
    LifecycleManager,
    LifecycleEvent,
    AIEvaluationEngine,
    DiagnosticsEngine,
    CircuitBreaker,
    tool
)

@tool(name="customer_search_tool", description="Search customer enterprise records")
def customer_search_tool(customer_id: str) -> str:
    return f"Record for Customer {customer_id}: Status=ACTIVE, Tier=PLATINUM"

class EnterpriseMetricsPlugin(FrameworkPlugin):
    @property
    def plugin_name(self) -> str:
        return "enterprise_metrics_plugin"

    @property
    def version(self) -> str:
        return "1.2.0"

    def initialize(self, container) -> bool:
        return True

async def main():
    print("=== Phase 27: Enterprise AI Governance, Model Routing & Resiliency ===")

    # 1. Diagnostics & Health Check
    print("\n--- 1. Diagnostics Engine Check ---")
    diag_report = DiagnosticsEngine.run_full_diagnostics()
    print(f"Diagnostics System Status: {'HEALTHY' if diag_report.is_healthy else 'UNHEALTHY'}")
    print(f"Total Checks Executed: {len(diag_report.checks)}")

    # 2. Environment Profile & Feature Flags
    print("\n--- 2. Environment Profiles & Feature Flags ---")
    env_mgr = EnvironmentProfileManager(current_env=EnvironmentType.PRODUCTION)
    prod_profile = env_mgr.get_profile()
    print(f"Active Environment: {prod_profile.env_type.value}")
    print(f"Fail-Fast Guardrails: {prod_profile.fail_fast_guardrails}")

    flags = FeatureFlagsManager(overrides={"EnableKafka": True, "EnableAudit": True})
    print(f"Feature Flag 'EnableKafka': {flags.is_enabled('EnableKafka')}")
    print(f"Feature Flag 'EnableRAG': {flags.is_enabled('EnableRAG')}")

    # 3. Extension SDK Plugin Validation
    print("\n--- 3. Framework Extension SDK ---")
    plugin = EnterpriseMetricsPlugin()
    is_valid = PluginValidator.validate_plugin(plugin)
    print(f"Plugin '{plugin.plugin_name}' (v{plugin.version}) Validated: {is_valid}")

    # 4. Centralized AI Policy Engine
    print("\n--- 4. AI Policy Engine Governance ---")
    policy = AIPolicy(
        allowed_tools=["customer_search_tool"],
        allowed_models=["gemini-3.6-flash"],
        max_prompt_tokens=8000
    )
    policy_engine = AIPolicyEngine(global_policy=policy)
    auth_res = policy_engine.validate_tool_access("customer_search_tool")
    print(f"Authorization for 'customer_search_tool': {'AUTHORIZED' if auth_res.is_success else 'DENIED'}")

    # 5. Developer Experience Fluent Builder API
    print("\n--- 5. Developer Experience Agent Builder ---")
    agent = (
        EnterpriseAgent.builder()
        .use_azure_openai()
        .use_memory()
        .use_redis()
        .use_kafka()
        .use_guardrails()
        .use_policy_engine(GuardrailPolicy(deny_tools=["drop_table"]))
        .use_streaming()
        .register_tool(customer_search_tool)
        .discover_mcp_servers()
        .build()
    )

    res = await agent.chat("Summarize customer 101's activity using customer_search_tool")
    print(f"Chat Execution Status: {res.value['status']}")
    print(f"Agent Response Output: {res.value['response']}")

    # 6. AI Evaluation Framework
    print("\n--- 6. AI Evaluation Framework Benchmarking ---")
    eval_engine = AIEvaluationEngine()
    eval_report = await eval_engine.run_evaluation(agent)
    print(f"Evaluation Summary: {json.dumps(eval_report['summary'], indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
