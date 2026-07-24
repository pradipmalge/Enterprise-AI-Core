# Messaging & gRPC Module (`enterprise_ai_core.messaging` & `enterprise_ai_core.grpc`)

The **Messaging & gRPC Module** provides event-driven communication and gRPC remote procedure call capabilities.

## Event Messaging (`enterprise_ai_core.messaging`)

### Supported Event Buses
1. `InMemoryEventBus`: Lightweight async event bus for single-node execution.
2. `KafkaEventBus`: Enterprise Apache Kafka bus for distributed event streaming.
3. `RabbitMQEventBus`: RabbitMQ message queue integration.

```python
bus = KafkaEventBus(bootstrap_servers="localhost:9092")
await bus.publish("agent-events", {"event": "AGENT_STARTED", "agent_id": "agent-101"})
```

---

## gRPC Services (`enterprise_ai_core.grpc`)

Provides gRPC protocol buffer definitions and server handlers for high-throughput microservice communication.
