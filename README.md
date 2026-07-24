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
