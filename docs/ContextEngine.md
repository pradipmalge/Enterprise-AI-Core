# Enterprise Context Engine Architecture

The **Enterprise Context Engine** is a core sub-system of `Enterprise-AI-Core`. It provides a provider-based, token-optimized context orchestration architecture to construct, validate, optimize, and render complete prompts before sending requests to Large Language Models.

```mermaid
graph TD
    A[User Request] --> B[ContextEngine]
    B --> C[ContextResolver]
    C --> D[ContextProviders Registry]
    D --> E1[SystemContextProvider]
    D --> E2[DeveloperContextProvider]
    D --> E3[ConversationContextProvider]
    D --> E4[KnowledgeContextProvider / RAG]
    D --> E5[MemoryContextProvider]
    D --> E6[ToolContextProvider]
    E1 & E2 & E3 & E4 & E5 & E6 --> F[Raw ContextEnvelope]
    F --> G[ContextValidationMiddleware]
    G --> H[PIIFiltering & Security Middleware]
    H --> I[TokenBudgetManager & ContextOptimizer]
    I --> J[ContextRenderer]
    J --> K[LLM Provider]
```

## Key Capabilities

- **Provider-Based Extension**: Implement `IContextProvider` to inject custom domain signals.
- **Priority-Based Token Budgeting**: Automatically drops or compresses low-priority fragments when prompt budgets are exceeded.
- **Middlewares**: Redacts PII, enforces security rules, and logs context metadata automatically.
- **Template Versioning**: Manages prompt templates (`v1.0`, `v2.0`, A/B tests) via `PromptTemplateEngine`.

## Usage Quickstart

```python
from enterprise_ai_core import EnterpriseAgent
from enterprise_ai_core.context import ContextEngine, SystemContextProvider

# Fluent Builder configuration
agent = (
    EnterpriseAgent.builder()
    .use_gemini()
    .with_system_prompt("You are a Senior Architect AI Agent.")
    .build()
)

result = await agent.chat("Analyze my Cloud SLA compliance.")
print(result.value["context_summary"])
```
