# Tool Security & Role-Based Authorization

Tools give AI agents agency to perform real actions (database queries, external API calls, transactional executions). The Guardrails Engine protects tool execution via **PreTool** and **PostTool** validation.

## Protections

1. **Tool Access Authorization**: Checks `allow_tools` and `deny_tools`.
2. **Role-Based Authorization**: Verifies user role passed in `agent.chat(query, user_role="...")`.
3. **Parameter Validation**: Prevents dangerous arguments.
4. **Result Inspection**: Ensures tool output does not leak unencrypted secrets or sensitive credentials.

```python
# Custom PreTool Guardrail Example
class CustomToolGuardrail(IPreToolGuardrail):
    @property
    def name(self) -> str:
        return "custom_tool_guardrail"

    async def validate_tool_call(self, tool_name: str, tool_args: dict, ctx: GuardrailContext) -> GuardrailResult:
        if tool_name == "transfer_funds" and tool_args.get("amount", 0) > 10000:
            if ctx.user_role != "executive":
                return GuardrailResult.block(self.name, GuardrailPhase.PRE_TOOL, "Transfers over $10,000 require executive role.")
        return GuardrailResult.allow()
```
