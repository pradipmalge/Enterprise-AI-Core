from typing import List, Any, Optional
import os
from enterprise_ai_core.agent.agent import EnterpriseAgent
from enterprise_ai_core.llm.interfaces import ILLMProvider
from enterprise_ai_core.llm.gemini_provider import GeminiLLMProvider
from enterprise_ai_core.llm.openai_provider import AzureOpenAIProvider, OpenAIProvider
from enterprise_ai_core.tools.registry import ToolRegistry
from enterprise_ai_core.tools.interfaces import ITool
from enterprise_ai_core.cache.memory_cache import MemoryCache, RedisCache
from enterprise_ai_core.cache.interfaces import ICache
from enterprise_ai_core.memory.conversation_memory import ConversationMemory
from enterprise_ai_core.memory.interfaces import IMemoryProvider
from enterprise_ai_core.messaging.in_memory_bus import InMemoryBus, KafkaBus, RabbitMQBus
from enterprise_ai_core.messaging.interfaces import IMessageBus
from enterprise_ai_core.mcp.client import MCPClient, MCPServerConfig
from enterprise_ai_core.context import ContextEngine, IContextProvider, SystemContextProvider
from enterprise_ai_core.guardrails import GuardrailsEngine, GuardrailPolicy, GuardrailConfiguration, IGuardrail

class AgentBuilder:
    def __init__(self):
        self._llm_provider: Optional[ILLMProvider] = None
        self._tool_registry = ToolRegistry()
        self._cache_provider: Optional[ICache] = None
        self._memory_provider: Optional[IMemoryProvider] = ConversationMemory()
        self._message_bus: Optional[IMessageBus] = None
        self._mcp_clients: List[MCPClient] = []
        self._system_prompt: str = "You are an Enterprise AI Agent operating under Clean Architecture."
        self._context_engine: Optional[ContextEngine] = None
        self._custom_context_providers: List[IContextProvider] = []
        self._guardrails_engine: Optional[GuardrailsEngine] = None
        self._guardrail_policy: Optional[GuardrailPolicy] = None
        self._custom_guardrails: List[IGuardrail] = []

    def use_gemini(self, api_key: Optional[str] = None, model: str = "gemini-3.6-flash") -> 'AgentBuilder':
        self._llm_provider = GeminiLLMProvider(api_key=api_key, model=model)
        return self

    def use_azure_openai(self, endpoint: Optional[str] = None, api_key: Optional[str] = None) -> 'AgentBuilder':
        self._llm_provider = AzureOpenAIProvider(endpoint=endpoint, api_key=api_key)
        return self

    def use_openai(self, api_key: Optional[str] = None, model: str = "gpt-4o") -> 'AgentBuilder':
        self._llm_provider = OpenAIProvider(api_key=api_key, model=model)
        return self

    def use_memory(self) -> 'AgentBuilder':
        self._memory_provider = ConversationMemory()
        return self

    def use_redis(self, redis_url: str = "redis://localhost:6379/0") -> 'AgentBuilder':
        return self.use_redis_cache(redis_url=redis_url)

    def use_kafka(self, bootstrap_servers: str = "localhost:9092") -> 'AgentBuilder':
        return self.use_kafka_bus(bootstrap_servers=bootstrap_servers)

    def use_guardrails(self) -> 'AgentBuilder':
        if not self._guardrails_engine:
            self._guardrails_engine = GuardrailsEngine()
        return self

    def use_policy_engine(self, policy: Optional[GuardrailPolicy] = None) -> 'AgentBuilder':
        if policy:
            self._guardrail_policy = policy
        return self

    def use_streaming(self) -> 'AgentBuilder':
        # Flag streaming preference
        return self

    def use_memory_cache(self) -> 'AgentBuilder':
        self._cache_provider = MemoryCache()
        return self

    def use_redis_cache(self, redis_url: str = "redis://localhost:6379/0") -> 'AgentBuilder':
        self._cache_provider = RedisCache(redis_url=redis_url)
        return self

    def use_in_memory_bus(self) -> 'AgentBuilder':
        self._message_bus = InMemoryBus()
        return self

    def use_kafka_bus(self, bootstrap_servers: str = "localhost:9092") -> 'AgentBuilder':
        self._message_bus = KafkaBus(bootstrap_servers=bootstrap_servers)
        return self

    def use_rabbitmq_bus(self, amqp_url: str = "amqp://guest:guest@localhost:5672/") -> 'AgentBuilder':
        self._message_bus = RabbitMQBus(amqp_url=amqp_url)
        return self

    def register_tool(self, tool_instance: ITool) -> 'AgentBuilder':
        self._tool_registry.register(tool_instance)
        return self

    def register_mcp_server(self, name: str, endpoint: str) -> 'AgentBuilder':
        config = MCPServerConfig(name=name, endpoint=endpoint)
        client = MCPClient(config)
        self._mcp_clients.append(client)
        return self

    def discover_mcp_servers(self) -> 'AgentBuilder':
        # Default enterprise MCP server discovery
        if not self._mcp_clients:
            self.register_mcp_server("enterprise_db_mcp", "http://mcp.internal.enterprise:8080")
            self.register_mcp_server("enterprise_docs_mcp", "http://docs-mcp.internal.enterprise:8080")
        return self

    def with_system_prompt(self, prompt: str) -> 'AgentBuilder':
        self._system_prompt = prompt
        return self

    def with_system_prompt_file(self, filepath: str) -> 'AgentBuilder':
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self._system_prompt = f.read()
        return self

    def with_system_context_provider(self, provider: IContextProvider) -> 'AgentBuilder':
        self._custom_context_providers.append(provider)
        return self

    def with_context_provider(self, provider: IContextProvider) -> 'AgentBuilder':
        self._custom_context_providers.append(provider)
        return self

    def with_context_engine(self, engine: ContextEngine) -> 'AgentBuilder':
        self._context_engine = engine
        return self

    def with_guardrails_engine(self, engine: GuardrailsEngine) -> 'AgentBuilder':
        self._guardrails_engine = engine
        return self

    def with_guardrail_policy(self, policy: GuardrailPolicy) -> 'AgentBuilder':
        self._guardrail_policy = policy
        return self

    def register_guardrail(self, guardrail: IGuardrail) -> 'AgentBuilder':
        self._custom_guardrails.append(guardrail)
        return self

    def build(self) -> EnterpriseAgent:
        if not self._llm_provider:
            self._llm_provider = GeminiLLMProvider()

        if not self._context_engine:
            self._context_engine = ContextEngine()
            if self._system_prompt:
                self._context_engine.register_provider(SystemContextProvider(self._system_prompt))
            for p in self._custom_context_providers:
                self._context_engine.register_provider(p)

        if not self._guardrails_engine:
            config = GuardrailConfiguration(policy=self._guardrail_policy) if self._guardrail_policy else GuardrailConfiguration()
            self._guardrails_engine = GuardrailsEngine(config=config)

        for g in self._custom_guardrails:
            self._guardrails_engine.register_guardrail(g)

        return EnterpriseAgent(
            llm_provider=self._llm_provider,
            tool_registry=self._tool_registry,
            memory_provider=self._memory_provider,
            cache_provider=self._cache_provider,
            message_bus=self._message_bus,
            mcp_clients=self._mcp_clients,
            system_prompt=self._system_prompt,
            context_engine=self._context_engine,
            guardrails_engine=self._guardrails_engine
        )
