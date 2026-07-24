import asyncio
import json
from enterprise_ai_core import EnterpriseAgent
from enterprise_ai_core.context import (
    ContextEngine,
    ContextBuilder,
    ContextPriority,
    ContextFragment,
    IContextProvider,
    PromptTemplateEngine,
    TokenBudgetManager,
    CustomContextProvider
)

# Define Custom Domain Context Provider
class SecurityComplianceContextProvider(IContextProvider):
    @property
    def name(self) -> str:
        return "security_compliance"

    async def provide_context(self, request: dict):
        return [
            ContextFragment(
                name="soc2_compliance_rules",
                content="[SECURITY_POLICY]\nSOC2 Type II & GDPR data processing guidelines active. Enforce HTTPS.",
                priority=ContextPriority.SAFETY_RULES,
                source="SecurityComplianceContextProvider"
            )
        ]

async def main():
    print("=== Phase 25: Enterprise Context Engine & Orchestration ===")

    # Step 1: Demonstrate Direct ContextEngine & Pipeline Execution
    print("\n[Step 1] Constructing ContextEngine with Custom Provider & Token Budget...")
    engine = (
        ContextEngine.builder()
        .with_system_prompt("You are Apex Financial Enterprise Agent operating under SOC2 compliance.")
        .with_developer_instructions("Always format numbers in USD format ($XX,XXX.XX).")
        .with_max_tokens(2048)
        .with_provider(SecurityComplianceContextProvider())
        .build()
    )

    request_payload = {
        "request_id": "req-ctx-991",
        "user_query": "What is the Q3 SLA penalty credit calculation?",
        "session_id": "sess-alpha-001",
        "session_metadata": {"tenant": "ApexCloud", "tier": "Enterprise"},
        "memory_facts": ["Customer preferred currency: USD", "Account manager: Sarah Jenkins"],
        "rag_chunks": [
            {"source": "Apex_SLA_2026.pdf", "content": "SLA Uptime Guarantee: 99.9%. Penalty Credit: 5% per 0.1% downtime."}
        ],
        "conversation_history": [
            {"role": "user", "content": "Hello agent."},
            {"role": "assistant", "content": "Hello! How can I assist with your Apex Cloud SLA today?"}
        ]
    }

    envelope = await engine.build_context(request_payload)

    print("\n=== GENERATED CONTEXT ENVELOPE SUMMARY ===")
    print(f"Request ID: {envelope.request_id}")
    print(f"Total Tokens: {envelope.total_tokens}")
    print(f"Fragments Count: {len(envelope.fragments)}")
    print("Active Fragment Names:")
    for f in envelope.fragments:
        print(f" - [{f.priority.name}] {f.name} ({f.tokens_estimated} tokens) from {f.source}")

    print("\n--- RENDERED SYSTEM PROMPT ---")
    print(envelope.system_prompt)

    print("\n--- RENDERED USER CONTEXT PROMPT ---")
    print(envelope.user_prompt)

    # Step 2: Prompt Template Engine & Versioning
    print("\n[Step 2] Testing Prompt Template Engine Variable Rendering & Versioning...")
    tmpl_engine = PromptTemplateEngine()
    rendered_plan = tmpl_engine.render("planner", {
        "query": "Audit Q3 AWS Invoices for anomalous charges",
        "tools": ["cloud_billing_api", "invoice_parser_tool"]
    })
    print("Rendered Planner Template:\n", rendered_plan)

    # Step 3: Enterprise Agent Integration via AgentBuilder
    print("\n[Step 3] Building Enterprise Agent with ContextEngine integrated...")
    agent = (
        EnterpriseAgent.builder()
        .use_gemini()
        .with_system_prompt("You are a Senior SLA Compliance Analyst.")
        .with_context_provider(SecurityComplianceContextProvider())
        .build()
    )

    res = await agent.chat("What is the penalty credit calculation in our Apex Cloud SLA contract?", session_id="sess-8871")
    print("\nAgent Output:")
    print(json.dumps(res.value, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
