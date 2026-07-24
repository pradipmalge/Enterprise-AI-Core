# Agent Module (`enterprise_ai_core.agent`)

The **Agent Module** provides the primary agent execution engine, orchestration facade, and fluent builder pattern for building enterprise AI assistants.

## Key Classes & Components

### `EnterpriseAgent`
The central execution facade that orchestrates planning, policy checks, context assembly, LLM execution, tool calling, memory updates, guardrail validations, and event lifecycle emissions.

#### Usage Example
```python
from enterprise_ai_core import EnterpriseAgent

response = await agent.chat("Analyze quarterly sales data.", user_role="analyst")
print(response.value["response"])
```

---

### `AgentBuilder` (`EnterpriseAgent.builder()`)
A fluent builder API that simplifies agent initialization with dependency injection, memory, caching, messaging, policies, and tool discovery.

#### Usage Example
```python
agent = (
    EnterpriseAgent.builder()
        .use_azure_openai()
        .use_memory()
        .use_redis()
        .use_kafka()
        .use_guardrails()
        .use_policy_engine()
        .use_streaming()
        .register_tool(my_tool)
        .discover_mcp_servers()
        .build()
)
```

---

### `AgentStep` & `ExecutionTrace`
Tracks intermediate steps, tool calls, observations, reasoning logs, and execution state throughout multi-step task execution.
