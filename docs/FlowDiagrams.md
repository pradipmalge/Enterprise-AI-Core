# Enterprise AI Core - System Flow Diagrams

This document contains flow diagrams illustrating the runtime execution paths across the Enterprise AI Core framework.

---

## 1. End-to-End Chat Request Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Agent as EnterpriseAgent
    participant Policy as AIPolicyEngine
    participant Guard as GuardrailsEngine
    participant Context as ContextEngine
    participant Router as ModelRoutingEngine
    participant LLM as LLM Provider Driver
    participant Tool as ToolRegistry / MCP
    participant Mem as Memory / Cache

    User->>Agent: chat(prompt, user_role)
    Agent->>Policy: validate_model_access & validate_tool_access
    alt Policy Denied
        Policy-->>Agent: Violation Error
        Agent-->>User: BLOCKED_BY_POLICY
    end

    Agent->>Guard: PreRequest Validation (Injection & PII Redaction)
    alt Guardrail Blocked
        Guard-->>Agent: Guardrail Violation
        Agent-->>User: BLOCKED_BY_GUARDRAIL
    end

    Agent->>Context: build_context_envelope(prompt, history, metadata)
    Context-->>Agent: Prioritized Context Envelope

    Agent->>Router: generate_text_with_failover(prompt)
    Router->>LLM: Call Primary Provider (e.g., Azure OpenAI)
    alt Primary Provider Fails
        Router->>LLM: Failover to Secondary Provider (e.g., Gemini)
    end
    LLM-->>Router: Response / Tool Call Request
    Router-->>Agent: Result Payload

    opt Agent executes Tool
        Agent->>Guard: PreTool Validation (RBAC & Tool Blacklist)
        Agent->>Tool: execute_tool(args)
        Tool-->>Agent: Observation Result
        Agent->>Guard: PostTool Inspection
    end

    Agent->>Guard: PostResponse Validation (Secrets & PII Redaction)
    Agent->>Mem: save_message(user_prompt, agent_response)
    Agent-->>User: Success Response Payload
```

---

## 2. 6-Stage Guardrail Pipeline Flow

```mermaid
graph TD
    A[Incoming User Query] --> B[1. PreRequest Guardrails]
    B -->|Check Prompt Injection & PII Redaction| C[2. PrePrompt Guardrails]
    C -->|Verify System Prompt & Token Budget| D[LLM Model Execution]
    D --> E[3. PostPrompt Guardrails]
    E -->|JSON Schema & Hallucination Check| F{Tool Execution Requested?}
    F -->|Yes| G[4. PreTool Guardrails]
    G -->|Validate Tool Perms & RBAC| H[Execute Tool / MCP]
    H --> I[5. PostTool Guardrails]
    I -->|Inspect Tool Observation| D
    F -->|No| J[6. PostResponse Guardrails]
    J -->|Redact Secrets & PII Scrubbing| K[Final Output Response to User]
```

---

## 3. Model Routing & Failover Flow

```mermaid
flowchart TD
    Req[Incoming LLM Request] --> Router[Model Routing Engine]
    Router --> Check[Get Healthy Providers Sorted by Priority & Latency]
    Check --> Candidate1[Attempt Primary Provider: Azure OpenAI]
    Candidate1 -->|Success| Resp[Return Result]
    Candidate1 -->|Failure / Timeout| Circuit1[Increment Failure Count]
    Circuit1 --> Candidate2[Failover to Secondary: Gemini 3.6 Flash]
    Candidate2 -->|Success| Resp
    Candidate2 -->|Failure| Candidate3[Failover to Tertiary: Ollama / Anthropic]
    Candidate3 -->|Success| Resp
    Candidate3 -->|All Failed| Fail[Return Failure Result]
```

---

## 4. Lifecycle Event Bus Flow

```mermaid
graph LR
    Sub[Framework Subscribers / Plugins] -->|Subscribe| Bus[Lifecycle Event Bus]
    Agent[Agent Execution Loop] -->|Emit BEFORE_REQUEST| Bus
    Agent -->|Emit BEFORE_LLM| Bus
    Agent -->|Emit AFTER_LLM| Bus
    Agent -->|Emit BEFORE_TOOL| Bus
    Agent -->|Emit AFTER_TOOL| Bus
    Agent -->|Emit AFTER_REQUEST| Bus
    Bus -->|Trigger Callbacks| Sub
```
