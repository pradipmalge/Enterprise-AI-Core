# Enterprise Guardrails Engine Architecture

The **Enterprise Guardrails Engine** protects AI applications before, during, and after LLM execution. It provides a modular, policy-driven, provider-based architecture for validating inputs, enforcing enterprise compliance, authorizing tool execution, redacting sensitive data, and auditing violations.

---

## 6-Stage Execution Pipeline

```
     User Request
          │
          ▼
1. PreRequest Guardrails       ─── [Block Injection, Jailbreak, Rate Limits]
          │
          ▼
   Context Engine
          │
          ▼
2. PrePrompt Guardrails        ─── [Verify System Prompt & Token Limits]
          │
          ▼
        LLM
          │
          ▼
3. PostPrompt Guardrails       ─── [Validate JSON / Output Quality]
          │
          ▼
4. PreTool Guardrails          ─── [Authorize Tool Access & Parameters]
          │
          ▼
     Tool Execution
          │
          ▼
5. PostTool Guardrails         ─── [Inspect Tool Results]
          │
          ▼
6. PostResponse Guardrails     ─── [Scrub PII & Redact Secrets]
          │
          ▼
   Return Response
```

---

## Key Interfaces

- `IPreRequestGuardrail`: Validates raw incoming user query string.
- `IPrePromptGuardrail`: Validates rendered system prompt and context envelope before LLM call.
- `IPostPromptGuardrail`: Validates LLM reasoning and generated text.
- `IPreToolGuardrail`: Authorizes tool execution and validates parameters/roles.
- `IPostToolGuardrail`: Validates tool observations before feeding back to context.
- `IPostResponseGuardrail`: Scrubs output response payload before returning to user.

---

## Policy Engine Configuration

Policies can be declared in Python, JSON, or YAML:

```yaml
policy:
  allow_tools:
    - WeatherTool
    - CustomerSearch
  deny_tools:
    - DeleteDatabase
  max_prompt_tokens: 8000
  max_response_tokens: 2000
  allowed_roles:
    - admin
    - operator
  enable_pii_redaction: true
  enable_prompt_injection_check: true
  enable_secrets_detection: true
```

---

## Example Usage

```python
from enterprise_ai_core import AgentBuilder, GuardrailsEngine, GuardrailPolicy, tool

@tool(name="DeleteDatabase", description="Deletes records")
def delete_db() -> str:
    return "Database deleted"

policy = GuardrailPolicy(
    deny_tools=["DeleteDatabase"],
    max_prompt_tokens=4000
)

agent = (
    AgentBuilder()
    .use_gemini()
    .with_guardrail_policy(policy)
    .register_tool(delete_db)
    .build()
)

res = await agent.chat("Please delete database", user_role="guest")
print(res.value["status"]) # BLOCKED_BY_GUARDRAIL
```
