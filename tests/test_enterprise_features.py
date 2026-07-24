import asyncio
import unittest
from enterprise_ai_core import (
    ModelRoutingEngine,
    AIPolicyEngine,
    AIPolicy,
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
    retry_with_backoff,
    EnterpriseAgent
)

class SamplePlugin(FrameworkPlugin):
    @property
    def plugin_name(self) -> str:
        return "sample_analytics_plugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, container) -> bool:
        return True

class TestEnterpriseCapabilities(unittest.TestCase):

    def test_feature_flags(self):
        ff = FeatureFlagsManager(overrides={"EnableKafka": True})
        self.assertTrue(ff.is_enabled("EnableKafka"))
        self.assertTrue(ff.is_enabled("EnableRAG"))
        ff.set_flag("EnableRAG", False)
        self.assertFalse(ff.is_enabled("EnableRAG"))

    def test_environment_profile(self):
        pm = EnvironmentProfileManager(current_env=EnvironmentType.PRODUCTION)
        profile = pm.get_profile()
        self.assertEqual(profile.env_type, EnvironmentType.PRODUCTION)
        self.assertTrue(profile.fail_fast_guardrails)

    def test_plugin_validator(self):
        plugin = SamplePlugin()
        self.assertTrue(PluginValidator.validate_plugin(plugin))

    def test_ai_policy_engine(self):
        policy = AIPolicy(
            allowed_tools=["customer_search"],
            allowed_models=["gemini-3.6-flash"]
        )
        engine = AIPolicyEngine(global_policy=policy)
        self.assertTrue(engine.validate_tool_access("customer_search").is_success)
        self.assertFalse(engine.validate_tool_access("unauthorized_tool").is_success)

    def test_diagnostics_engine(self):
        report = DiagnosticsEngine.run_full_diagnostics()
        self.assertTrue(report.is_healthy)
        self.assertGreater(len(report.checks), 0)

    def test_circuit_breaker(self):
        async def run_cb():
            cb = CircuitBreaker(failure_threshold=2)
            
            async def succeed():
                return "OK"

            async def fail():
                raise ValueError("Error")

            res = await cb.execute(succeed)
            self.assertEqual(res, "OK")

            try:
                await cb.execute(fail)
            except ValueError:
                pass

            try:
                await cb.execute(fail)
            except ValueError:
                pass

            self.assertEqual(cb.state, "OPEN")

        asyncio.run(run_cb())

    def test_fluent_agent_builder(self):
        agent = (
            EnterpriseAgent.builder()
            .use_gemini()
            .use_memory()
            .use_redis()
            .use_kafka()
            .use_guardrails()
            .use_streaming()
            .discover_mcp_servers()
            .build()
        )
        self.assertIsNotNone(agent)

if __name__ == "__main__":
    unittest.main()
