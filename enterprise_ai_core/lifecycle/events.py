import asyncio
import logging
from enum import Enum
from typing import Dict, Any, List, Callable, Awaitable

logger = logging.getLogger("FrameworkLifecycle")

class LifecycleEvent(str, Enum):
    BEFORE_REQUEST = "BEFORE_REQUEST"
    AFTER_REQUEST = "AFTER_REQUEST"
    BEFORE_LLM = "BEFORE_LLM"
    AFTER_LLM = "AFTER_LLM"
    BEFORE_TOOL = "BEFORE_TOOL"
    AFTER_TOOL = "AFTER_TOOL"
    BEFORE_WORKFLOW = "BEFORE_WORKFLOW"
    AFTER_WORKFLOW = "AFTER_WORKFLOW"
    ON_RETRY = "ON_RETRY"
    ON_FAILURE = "ON_FAILURE"
    ON_CANCELLATION = "ON_CANCELLATION"
    ON_STREAMING_STARTED = "ON_STREAMING_STARTED"
    ON_STREAMING_COMPLETED = "ON_STREAMING_COMPLETED"

class LifecycleManager:
    """Central event bus for framework lifecycle subscriptions and execution hooks."""

    def __init__(self):
        self._listeners: Dict[LifecycleEvent, List[Callable[[Dict[str, Any]], Awaitable[None]]]] = {
            event: [] for event in LifecycleEvent
        }

    def subscribe(self, event: LifecycleEvent, callback: Callable[[Dict[str, Any]], Awaitable[None]]):
        self._listeners[event].append(callback)

    async def emit(self, event: LifecycleEvent, payload: Dict[str, Any]):
        listeners = self._listeners.get(event, [])
        for listener in listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(payload)
                else:
                    listener(payload)
            except Exception as ex:
                logger.error(f"Error in lifecycle subscriber for event {event.value}: {ex}")
