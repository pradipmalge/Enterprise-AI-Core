# System Context Configuration

System context defines agent identity, domain operational rules, and safety constraints.

## Configuration Options

1. **Inline String**:
```python
agent = EnterpriseAgent.builder().with_system_prompt("You are a Financial Auditor.").build()
```

2. **File-Based**:
```python
agent = EnterpriseAgent.builder().with_system_prompt_file("prompts/system.md").build()
```

3. **Custom Provider**:
```python
class CustomSystemProvider(IContextProvider):
    @property
    def name(self): return "custom_system"
    async def provide_context(self, req):
        return [ContextFragment("system", "Dynamic System Context", priority=ContextPriority.SYSTEM_PROMPT)]

agent = EnterpriseAgent.builder().with_system_context_provider(CustomSystemProvider()).build()
```
