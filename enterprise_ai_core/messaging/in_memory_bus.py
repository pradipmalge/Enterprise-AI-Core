import asyncio
from typing import Callable, Dict, List, Any
from enterprise_ai_core.messaging.interfaces import IMessageBus

class InMemoryBus(IMessageBus):
    def __init__(self):
        self._subscriptions: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        handlers = self._subscriptions.get(topic, [])
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(message)
            else:
                handler(message)

    async def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        if topic not in self._subscriptions:
            self._subscriptions[topic] = []
        self._subscriptions[topic].append(handler)

class KafkaBus(IMessageBus):
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        self._fallback = InMemoryBus()

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        await self._fallback.publish(topic, message)

    async def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        await self._fallback.subscribe(topic, handler)

class RabbitMQBus(IMessageBus):
    def __init__(self, amqp_url: str = "amqp://guest:guest@localhost:5672/"):
        self.amqp_url = amqp_url
        self._fallback = InMemoryBus()

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        await self._fallback.publish(topic, message)

    async def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        await self._fallback.subscribe(topic, handler)
