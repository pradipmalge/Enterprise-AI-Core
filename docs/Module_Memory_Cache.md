# Memory & Cache Module (`enterprise_ai_core.memory` & `enterprise_ai_core.cache`)

The **Memory & Cache Module** manages short-term and long-term conversation state, session windows, and high-performance caching.

## Memory Subsystem (`enterprise_ai_core.memory`)

### `ConversationMemory`
Maintains message history, sliding context windows, and user interaction turns per session.

```python
memory = ConversationMemory(max_history_turns=10)
memory.add_user_message("Hello AI")
memory.add_assistant_message("Hello! How can I assist you?")
```

---

## Cache Subsystem (`enterprise_ai_core.cache`)

### `MemoryCache`
In-memory TTL-based cache provider for rapid prompt, response, and embedding lookup.

### `RedisCache`
Distributed Redis driver for multi-instance application deployments.

```python
cache = RedisCache(redis_url="redis://localhost:6379/0")
await cache.set("key", "value", ttl_seconds=300)
val = await cache.get("key")
```
