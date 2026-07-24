# AI Governance, Policy Engine & Feature Flags

Enterprise AI Core features centralized policy enforcement, runtime feature flags, and environment profiles.

## Capabilities

1. **Centralized AI Policy Engine**: Declares allowed tools, models, MCP servers, plugins, and token limits.
2. **Feature Flags**: Toggle features (`EnableRAG`, `EnableMemory`, `EnableKafka`, `EnableAudit`) at runtime without code changes.
3. **Environment Profiles**: Configuration profiles for `DEVELOPMENT`, `TESTING`, `QA`, `STAGING`, and `PRODUCTION`.
4. **Extension SDK**: Create modular plugins via `FrameworkPlugin` and `PluginValidator`.

```python
from enterprise_ai_core import AIPolicyEngine, AIPolicy, FeatureFlagsManager

policy = AIPolicy(allowed_tools=["search_tool"], max_prompt_tokens=8000)
engine = AIPolicyEngine(global_policy=policy)

flags = FeatureFlagsManager(overrides={"EnableKafka": True})
```
