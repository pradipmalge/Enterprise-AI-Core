# Conversation Context & Multi-turn Management

`ConversationContextProvider` formats chat history and injects multi-turn dialogue into the context envelope under `ContextPriority.CONVERSATION_HISTORY`.

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Memory
    participant ContextEngine

    User->>Agent: Send Query
    Agent->>Memory: Fetch History(session_id)
    Memory-->>Agent: [User: Hi, Assistant: Hello]
    Agent->>ContextEngine: build_context({conversation_history})
    ContextEngine-->>Agent: Optimized ContextEnvelope
    Agent->>LLM: Generate Response
```
