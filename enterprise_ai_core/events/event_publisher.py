from typing import Dict, Any, Optional
import time
from enterprise_ai_core.messaging.interfaces import IMessageBus

class EventPublisher:
    def __init__(self, message_bus: Optional[IMessageBus] = None):
        self.bus = message_bus

    async def publish_event(self, event_type: str, payload: Dict[str, Any], topic: str = "ai.events") -> None:
        event_data = {
            "event_type": event_type,
            "timestamp": time.time(),
            "payload": payload
        }
        if self.bus:
            await self.bus.publish(topic, event_data)
