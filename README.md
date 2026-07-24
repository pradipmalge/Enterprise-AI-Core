# Enterprise AI Core Framework (v1.0)

An enterprise-grade Python framework for developing AI Chatbots, AI Agents, Tool Calling, MCP Integration, and AI Applications. Built upon Clean Architecture, SOLID principles, Dependency Injection, and modern async Python patterns.

## 🚀 Quick Start

```python
import asyncio
from enterprise_ai_core import EnterpriseAgent, tool

@tool(name="customer_search", description="Lookup customer in CRM")
def customer_search(customer_id: str) -> str:
    return f"Customer {customer_id}: Enterprise Plan, Status=Active, Value=$250k"

async def main():
    agent = (
        EnterpriseAgent.builder()
            .use_azure_openai()
            .use_memory_cache()
            .use_in_memory_bus()
            .register_tool(customer_search)
            .discover_mcp_servers()
            .build()
    )

    response = await agent.chat("Find customer 101 and summarize their status.")
    print(response.value["response"])

if __name__ == "__main__":
    asyncio.run(main())
```

## 🏗️ Architectural Overview

- **Clean Architecture Layers**: Domain Abstractions -> Core Engine -> Infrastructure Providers -> Presentation / API.
- **Dependency Injection**: Integrated IoC container (`ServiceCollection`, `ServiceProvider`).
- **Fluent Builder API**: Instantiate production agents in under 15 lines of code.
- **Model Context Protocol (MCP)**: Dynamic tool discovery & server session management.
- **Event-Driven Messaging**: Support for InMemory, Apache Kafka, and RabbitMQ event buses.
- **Extensible Storage & Caching**: TTL memory cache, Redis distributed caching, and session windows.

## 📚 Documentation & System Diagrams Index

### 📐 System Architecture & Flow Diagrams
- [System Architecture Specification](docs/SystemArchitecture.md) — Clean Architecture layers, subsystem integration diagrams.
- [System Flow Diagrams](docs/FlowDiagrams.md) — Sequence & flowcharts for end-to-end chat, guardrails pipeline, model routing, and lifecycle events.
- [Architecture Layers](docs/Architecture.md) — High-level clean architecture layers.

### 🛡️ Guardrails & Security Engine
- [Guardrails Engine Architecture](docs/Guardrails.md) — 6-stage execution pipeline specification.
- [Prompt Injection Defense](docs/PromptInjection.md) — Jailbreak detection and threat vector mitigation.
- [Tool Security & Authorization](docs/ToolSecurity.md) — RBAC, tool whitelisting/blacklisting.
- [PII & Secret Protection](docs/PIIProtection.md) — Automated SSN, email, phone, and credential scrubbing.
- [Security Policies](docs/SecurityPolicies.md) — Policy configuration, token limits, and compliance enforcement.
- [Compliance & Audit Logging](docs/Compliance.md) — SOC2, HIPAA, and GDPR audit event schemas.

### ⚙️ Governance, Routing & Management
- [Enterprise Model Routing](docs/ModelRouting.md) — Multi-provider routing, priority, and automatic failover.
- [AI Governance & Policy Engine](docs/Governance.md) — Centralized policy engine, feature flags, and environment profiles.
- [Enterprise Context Engine](docs/ContextEngine.md) — Priority token budgeting and context envelope management.
- [Token Management](docs/TokenManagement.md) — Context window allocation and priority token optimization.
- [Prompt Templates & Best Practices](docs/PromptTemplates.md) — Dynamic prompt templates and variables.

### 📦 Module Technical Documentation
- [Agent Module (`agent`)](docs/Module_Agent.md) — `EnterpriseAgent`, `AgentBuilder`, steps, and execution tracing.
- [LLM Module (`llm`)](docs/Module_LLM.md) — Drivers for Gemini, Azure OpenAI, OpenAI, Ollama, and Anthropic.
- [Tools & MCP Module (`tools` & `mcp`)](docs/Module_Tools_MCP.md) — `@tool` decorator, schema generator, registry, and MCP client.
- [Memory & Cache Module (`memory` & `cache`)](docs/Module_Memory_Cache.md) — Conversation memory, TTL cache, and Redis driver.
- [Messaging & gRPC Module (`messaging` & `grpc`)](docs/Module_Messaging_GRPC.md) — Event buses (Kafka, RabbitMQ, InMemory) and gRPC handlers.
- [Resiliency & Model Routing Module (`resiliency` & `routing`)](docs/Module_Resiliency_Routing.md) — Circuit breaker, exponential backoff retries, and router.
- [Diagnostics & AI Evaluation Module (`diagnostics` & `eval`)](docs/Module_Diagnostics_Eval.md) — System health diagnostics and AI evaluation framework.
- [Extension SDK & Lifecycle Module (`extension_sdk` & `lifecycle`)](docs/Module_Extension_SDK_Lifecycle.md) — Framework plugins and lifecycle event bus hooks.
- [RAG & Vector Search Module (`rag`)](docs/Module_RAG.md) — Document extractor and vector embedding store.

## 📁 Repository Structure

```
enterprise-ai-core/
├── enterprise_ai_core/    # Core Framework Source
│   ├── agent/             # Agent Execution Engine & Builder
│   ├── chat/              # Chat Engine & Prompt Management
│   ├── llm/               # LLM Provider Drivers (Gemini, Azure, OpenAI)
│   ├── memory/            # Conversation & Session Memory
│   ├── tools/             # Tool Registry, Schema Generator & Decorators
│   ├── mcp/               # Model Context Protocol Client & Discovery
│   ├── grpc/              # gRPC Service Definitions & Handlers
│   ├── cache/             # In-Memory & Redis Cache Drivers
│   ├── messaging/         # Kafka, RabbitMQ & In-Memory Event Buses
│   └── common/            # DI Container, Context & Result Patterns
├── docs/                  # Comprehensive Architecture & Developer Docs
├── tests/                 # Framework Unit & Integration Tests
└── examples/              # 15 Independent Runnable Examples
```
