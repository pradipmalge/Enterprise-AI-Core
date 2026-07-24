# Enterprise Compliance & Auditing

The Enterprise Guardrails Engine includes auditing capabilities to meet SOC2, HIPAA, and GDPR compliance standards.

## Audit Logs

Every guardrail evaluation generates structured audit logs containing:
- Request ID and Agent ID
- Timestamp
- Pipeline phase
- Violation reports and severity
- Action taken (ALLOW, MODIFY, BLOCK, WARN)

```json
{
  "request_id": "req-grd-a1b2c3",
  "agent_id": "agent-core",
  "user_role": "analyst",
  "timestamp": 1774300000,
  "violations": [
    {
      "id": "viol-99a2b1",
      "guardrail_name": "prompt_injection_guardrail",
      "phase": "PRE_REQUEST",
      "message": "Prompt injection vector detected in request.",
      "severity": "CRITICAL"
    }
  ]
}
```
