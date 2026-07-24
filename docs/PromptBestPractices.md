# Enterprise Prompt Engineering Best Practices

1. **Avoid String Concatenation**: Always use `ContextEngine` and `PromptTemplateEngine` instead of manually formatting prompt strings.
2. **Keep System Prompts Modular**: Use `SystemContextProvider` and `DeveloperContextProvider` to separate operational rules from core persona.
3. **Set Token Reserves**: Always leave at least 1,024 tokens reserved for LLM generation response.
4. **Use PII Middlewares**: Enable `PIIFilteringMiddleware` and `SensitiveDataRemovalMiddleware` in production environments.
5. **Version Templates**: Keep prompt templates versioned (`v1.0`, `v2.0`) in `/prompts/` to support seamless A/B tests and rollback capability.
