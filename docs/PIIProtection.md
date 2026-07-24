# PII & Secrets Leakage Protection

The `PIIGuardrail` and `SecretsGuardrail` safeguard privacy and security across all pipeline stages.

## Redacted Data Types

- **Personally Identifiable Information (PII)**:
  - Email addresses (`[REDACTED_EMAIL]`)
  - Phone numbers (`[REDACTED_PHONE]`)
  - Social Security Numbers (`[REDACTED_SSN]`)
- **Secrets & API Credentials**:
  - API Keys
  - Bearer Tokens
  - Passwords and Private Keys (`[REDACTED_SECRET]`)

## Automatic Scrubbing
Redaction occurs automatically on both input queries and output responses before returning data to users or logs.
