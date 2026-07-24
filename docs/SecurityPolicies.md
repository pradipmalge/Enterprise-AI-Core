# Security Policies & Policy Engine

The Enterprise AI Core Security Policy Engine allows declarative specification of enterprise compliance controls.

## Features

- **Tool Whitelisting & Blacklisting**: `allow_tools` and `deny_tools` lists.
- **Role-Based Access Control (RBAC)**: Validates user permissions against `allowed_roles`.
- **Token Limits**: Enforces `max_prompt_tokens` and `max_response_tokens`.
- **Automated PII & Secrets Detection**: Redacts SSNs, emails, API keys, and bearer tokens.

## Loading Policies

Policies can be loaded dynamically at runtime:

```python
from enterprise_ai_core.guardrails import GuardrailPolicyEngine

yaml_policy = """
policies:
  deny_tools:
    - ExecuteShellCommand
  allowed_roles:
    - Analyst
    - Admin
  enable_pii_redaction: true
"""

policy = GuardrailPolicyEngine.load_from_yaml(yaml_policy)
```
