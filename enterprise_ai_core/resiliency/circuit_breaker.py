import time
import asyncio
import logging
from typing import Callable, Any, TypeVar, Awaitable

logger = logging.getLogger("EnterpriseResiliency")

T = TypeVar("T")

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    """Enterprise Circuit Breaker pattern implementation."""

    def __init__(self, failure_threshold: int = 5, recovery_time_sec: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    async def execute(self, func: Callable[[], Awaitable[T]]) -> T:
        now = time.time()

        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_time_sec:
                self.state = "HALF-OPEN"
                logger.info("Circuit breaker entering HALF-OPEN state...")
            else:
                raise CircuitBreakerOpenException("Circuit breaker is OPEN. Requests blocked for safety.")

        try:
            res = await func()
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                logger.info("Circuit breaker successfully recovered to CLOSED state.")
            return res
        except Exception as ex:
            self.failure_count += 1
            self.last_failure_time = now
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.error(f"Circuit breaker tripped OPEN! Failure count: {self.failure_count}")
            raise ex

async def retry_with_backoff(
    func: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    initial_delay_sec: float = 0.5,
    backoff_factor: float = 2.0
) -> T:
    """Executes asynchronous operation with exponential backoff retries."""
    delay = initial_delay_sec
    last_ex = None

    for attempt in range(1, max_retries + 1):
        try:
            return await func()
        except Exception as ex:
            last_ex = ex
            logger.warning(f"Attempt {attempt}/{max_retries} failed: {ex}. Retrying in {delay}s...")
            if attempt < max_retries:
                await asyncio.sleep(delay)
                delay *= backoff_factor

    raise last_ex or Exception("Max retries exceeded")
