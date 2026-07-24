# Resiliency & Model Routing Module (`enterprise_ai_core.resiliency` & `enterprise_ai_core.routing`)

The **Resiliency & Model Routing Module** provides enterprise fault tolerance, circuit breaking, exponential backoff retries, and multi-provider LLM failover routing.

## Resiliency (`enterprise_ai_core.resiliency`)

### Circuit Breaker
Prevents cascading failures by opening when a service threshold of consecutive errors is reached.

```python
from enterprise_ai_core import CircuitBreaker

cb = CircuitBreaker(failure_threshold=5, recovery_time_sec=30.0)
result = await cb.execute(async_func)
```

### Exponential Backoff Retry
Retries transient operations with exponential delay.

```python
from enterprise_ai_core import retry_with_backoff

res = await retry_with_backoff(async_operation, max_retries=3)
```

---

## Model Routing Engine (`enterprise_ai_core.routing`)

Routes requests across multiple LLM providers (Azure OpenAI, Gemini, OpenAI, Ollama) with health checks, provider priority, and automatic failover.
