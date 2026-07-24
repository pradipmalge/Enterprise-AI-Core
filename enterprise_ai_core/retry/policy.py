import asyncio
import time
from typing import Callable, Any, Type, Tuple, Optional
from enterprise_ai_core.common.result import Result

class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        backoff_factor: float = 1.5,
        retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.retryable_exceptions = retryable_exceptions

    async def execute_async(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        attempt = 0
        delay = 0.5
        last_exception = None
        while attempt < self.max_attempts:
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except self.retryable_exceptions as ex:
                attempt += 1
                last_exception = ex
                if attempt >= self.max_attempts:
                    break
                await asyncio.sleep(delay)
                delay *= self.backoff_factor

        raise last_exception or Exception("Retry execution failed.")

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_time_sec: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_failure_time = 0.0

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_time_sec:
                self.state = "HALF-OPEN"
                return True
            return False
        return True  # HALF-OPEN allows probe request

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
