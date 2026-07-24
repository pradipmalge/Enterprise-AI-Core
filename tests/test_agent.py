import unittest
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enterprise_ai_core import EnterpriseAgent, tool, ServiceCollection, Result
from enterprise_ai_core.rag import (
    ingest_document_to_rag,
    extract_document_details,
    search_knowledge_base,
    VectorStore,
    DocumentLoader,
)
from enterprise_ai_core.context import (
    ContextEngine,
    PromptTemplateEngine,
    ContextPriority,
    ContextFragment,
    IContextProvider,
)

@tool(name="unit_test_tool", description="Test tool")
def unit_test_tool(x: int) -> str:
    return f"Result: {x * 2}"

class TestEnterpriseAICore(unittest.TestCase):
    def test_di_container(self):
        services = ServiceCollection()
        services.add_singleton("config", {"env": "test"})
        provider = services.build_service_provider()
        config = provider.get_service("config")
        self.assertEqual(config["env"], "test")

    def test_rag_pipeline_and_extraction(self):
        sample_doc = "SLA agreement effective March 1, 2026. Guarantee uptime is 99.99%. Contract value is $1,200,000 USD."
        ingest_res = ingest_document_to_rag(sample_doc, source_name="test_contract.txt")
        self.assertIn("INGESTED_AND_INDEXED", ingest_res)

        details = extract_document_details(sample_doc)
        self.assertIn("99.99%", details)
        self.assertIn("$1,200,000 USD", details)

        search_res = search_knowledge_base("uptime guarantee")
        self.assertIn("matches", search_res)

    def test_context_engine_and_templates(self):
        async def run_ctx_test():
            engine = (
                ContextEngine.builder()
                .with_system_prompt("System Test Prompt")
                .with_developer_instructions("Dev Rule 101")
                .with_max_tokens(1024)
                .build()
            )
            envelope = await engine.build_context({"user_query": "Hello Context Engine"})
            self.assertGreater(envelope.total_tokens, 0)
            self.assertIn("System Test Prompt", envelope.system_prompt)
            self.assertIn("Hello Context Engine", envelope.user_prompt)

            tmpl_engine = PromptTemplateEngine()
            rendered = tmpl_engine.render("planner", {"query": "Test Query", "tools": "Tool A"})
            self.assertIn("Test Query", rendered)

        asyncio.run(run_ctx_test())

    def test_agent_builder_and_execution(self):
        async def run_test():
            agent = (
                EnterpriseAgent.builder()
                    .use_gemini()
                    .use_memory_cache()
                    .register_tool(unit_test_tool)
                    .build()
            )
            result = await agent.chat("Test query")
            self.assertTrue(result.is_success)
            self.assertEqual(result.value["status"], "SUCCESS")
            self.assertIn("response", result.value)
            self.assertIn("context_summary", result.value)

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
