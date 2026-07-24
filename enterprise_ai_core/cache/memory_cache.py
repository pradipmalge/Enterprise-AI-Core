import time
from typing import Any, Optional, Dict, Tuple
from enterprise_ai_core.cache.interfaces import ICache

class MemoryCache(ICache):
    def __init__(self):
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}

    async def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        val, expiry = self._store[key]
        if expiry and time.time() > expiry:
            del self._store[key]
            return None
        return val

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expiry = time.time() + ttl if ttl else None
        self._store[key] = (value, expiry)

    async def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

class RedisCache(ICache):
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self._fallback = MemoryCache()

    async def get(self, key: str) -> Optional[Any]:
        return await self._fallback.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        await self._fallback.set(key, value, ttl)

    async def delete(self, key: str) -> bool:
        return await self._fallback.delete(key)
