# Model Routing Engine Architecture

The Enterprise Model Routing Engine provides multi-provider LLM orchestration with automatic failover, health checks, and latency-aware routing.

## Key Features

- **Supported Providers**: Azure OpenAI, OpenAI, Anthropic, Gemini, Ollama.
- **Automatic Failover**: Dynamically routes around failed or rate-limited endpoints.
- **Provider Priority & Capability**: Routes requests based on required capabilities (e.g. `FUNCTION_CALLING`, `VISION`, `STREAMING`).
- **Health Monitoring & Circuit Breaking**: Tracks average latencies and failure counts per provider.

```python
from enterprise_ai_core import ModelRoutingEngine, ProviderCapability

router = ModelRoutingEngine()
router.register_provider("azure_primary", azure_provider, priority=1)
router.register_provider("gemini_backup", gemini_provider, priority=2)

res = await router.generate_text_with_failover(
    "Summarize document",
    required_capability=ProviderCapability.TEXT_GENERATION
)
```
