import time
import asyncio
import logging
from enum import Enum
from typing import Dict, Any, List, Optional, Callable
from enterprise_ai_core.llm.interfaces import ILLMProvider
from enterprise_ai_core.common.result import Result

logger = logging.getLogger("EnterpriseModelRouting")

class ProviderHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"

class ProviderCapability(str, Enum):
    TEXT_GENERATION = "TEXT_GENERATION"
    CHAT = "CHAT"
    STREAMING = "STREAMING"
    FUNCTION_CALLING = "FUNCTION_CALLING"
    VISION = "VISION"
    EMBEDDINGS = "EMBEDDINGS"

class ManagedProvider:
    def __init__(
        self,
        name: str,
        provider: ILLMProvider,
        priority: int = 1,
        capabilities: Optional[List[ProviderCapability]] = None
    ):
        self.name = name
        self.provider = provider
        self.priority = priority
        self.capabilities = capabilities or [
            ProviderCapability.TEXT_GENERATION,
            ProviderCapability.CHAT,
            ProviderCapability.FUNCTION_CALLING
        ]
        self.status = ProviderHealthStatus.HEALTHY
        self.latency_ms_history: List[float] = []
        self.failure_count = 0

    @property
    def average_latency_ms(self) -> float:
        if not self.latency_ms_history:
            return 0.0
        return sum(self.latency_ms_history[-10:]) / len(self.latency_ms_history[-10:])

class ModelRoutingEngine:
    """Enterprise Model Router with failover, health monitoring, and latency-aware routing."""

    def __init__(self, primary_provider: Optional[ILLMProvider] = None):
        self.providers: Dict[str, ManagedProvider] = {}
        if primary_provider:
            self.register_provider("primary_gemini", primary_provider, priority=1)

    def register_provider(
        self,
        name: str,
        provider: ILLMProvider,
        priority: int = 1,
        capabilities: Optional[List[ProviderCapability]] = None
    ):
        self.providers[name] = ManagedProvider(name, provider, priority, capabilities)
        logger.info(f"Registered provider '{name}' with priority {priority}")

    def get_healthy_providers(self, required_capability: Optional[ProviderCapability] = None) -> List[ManagedProvider]:
        healthy = [
            p for p in self.providers.values()
            if p.status != ProviderHealthStatus.UNHEALTHY
        ]
        if required_capability:
            healthy = [p for p in healthy if required_capability in p.capabilities]
        
        # Sort by priority ascending, then latency
        return sorted(healthy, key=lambda x: (x.priority, x.average_latency_ms))

    async def generate_text_with_failover(
        self,
        prompt: str,
        required_capability: Optional[ProviderCapability] = ProviderCapability.TEXT_GENERATION,
        **kwargs
    ) -> Result[str]:
        candidates = self.get_healthy_providers(required_capability)
        if not candidates:
            return Result.fail("No healthy LLM providers available for routing.")

        errors = []
        for p in candidates:
            t0 = time.time()
            try:
                res = await p.provider.generate_text(prompt, **kwargs)
                lat = (time.time() - t0) * 1000
                p.latency_ms_history.append(lat)
                p.failure_count = 0
                p.status = ProviderHealthStatus.HEALTHY
                return res
            except Exception as ex:
                lat = (time.time() - t0) * 1000
                p.failure_count += 1
                if p.failure_count >= 3:
                    p.status = ProviderHealthStatus.UNHEALTHY
                errors.append(f"[{p.name}] {str(ex)}")
                logger.warning(f"Provider {p.name} failed: {ex}. Failover to next candidate.")

        return Result.fail(f"All routed providers failed: {'; '.join(errors)}")
