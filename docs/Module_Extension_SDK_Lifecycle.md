# Extension SDK & Lifecycle Module (`enterprise_ai_core.extension_sdk` & `enterprise_ai_core.lifecycle`)

The **Extension SDK & Lifecycle Module** provides developer plugin interfaces and framework event hook subscriptions.

## Extension SDK (`enterprise_ai_core.extension_sdk`)

Allows third-party developers to create framework extensions without modifying framework core code.

```python
from enterprise_ai_core import FrameworkPlugin, PluginValidator

class CustomAnalyticsPlugin(FrameworkPlugin):
    @property
    def plugin_name(self) -> str:
        return "custom_analytics"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, container) -> bool:
        return True

PluginValidator.validate_plugin(CustomAnalyticsPlugin())
```

---

## Lifecycle Event Bus (`enterprise_ai_core.lifecycle`)

Provides event hooks for framework state changes.

### Lifecycle Events
- `BEFORE_REQUEST` / `AFTER_REQUEST`
- `BEFORE_LLM` / `AFTER_LLM`
- `BEFORE_TOOL` / `AFTER_TOOL`
- `BEFORE_WORKFLOW` / `AFTER_WORKFLOW`
- `ON_RETRY` / `ON_FAILURE` / `ON_CANCELLATION`

```python
from enterprise_ai_core import LifecycleManager, LifecycleEvent

mgr = LifecycleManager()
mgr.subscribe(LifecycleEvent.BEFORE_LLM, lambda payload: print("Executing LLM call..."))
```
