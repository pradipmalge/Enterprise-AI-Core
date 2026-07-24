import os
import uuid
import asyncio
from typing import Dict, Any, List, Optional, Union
from .models import ContextEnvelope, ContextFragment, ContextPriority
from .interfaces import IContextProvider, IContextFilter, IContextTransformer, IContextOptimizer, IContextStore
from .providers import (
    SystemContextProvider,
    DeveloperContextProvider,
    ConversationContextProvider,
    UserContextProvider,
    SessionContextProvider,
    MemoryContextProvider,
    KnowledgeContextProvider,
    DocumentContextProvider,
    ToolContextProvider,
    AgentContextProvider,
    ExecutionContextProvider,
    RequestContextProvider,
    ResponseContextProvider,
    CustomContextProvider
)
from .templates import PromptTemplateEngine, PromptRenderer
from .token_budget import TokenBudgetManager, ContextOptimizer
from .middleware import (
    ContextValidationMiddleware,
    PIIFilteringMiddleware,
    SensitiveDataRemovalMiddleware,
    PromptLoggingMiddleware,
    ContextEnrichmentMiddleware
)

class ContextRegistry:
    """Enterprise Registry holding all context providers, prompt templates, and middleware."""
    
    def __init__(self):
        self.providers: Dict[str, IContextProvider] = {}
        self.filters: List[IContextFilter] = []
        self.transformers: List[IContextTransformer] = []
        self._register_default_providers()
        self._register_default_middlewares()

    def _register_default_providers(self):
        defaults = [
            SystemContextProvider(),
            DeveloperContextProvider(),
            ConversationContextProvider(),
            UserContextProvider(),
            SessionContextProvider(),
            MemoryContextProvider(),
            KnowledgeContextProvider(),
            DocumentContextProvider(),
            ToolContextProvider(),
            AgentContextProvider(),
            ExecutionContextProvider(),
            RequestContextProvider(),
            ResponseContextProvider(),
        ]
        for p in defaults:
            self.register_provider(p)

    def _register_default_middlewares(self):
        self.filters.append(ContextValidationMiddleware())
        self.filters.append(PIIFilteringMiddleware())
        self.filters.append(SensitiveDataRemovalMiddleware())
        self.transformers.append(PromptLoggingMiddleware())
        self.transformers.append(ContextEnrichmentMiddleware())

    def register_provider(self, provider: IContextProvider):
        self.providers[provider.name] = provider

    def register_filter(self, filter_middleware: IContextFilter):
        self.filters.append(filter_middleware)

    def register_transformer(self, transformer_middleware: IContextTransformer):
        self.transformers.append(transformer_middleware)

class ContextResolver:
    """Resolves and executes active providers for a request payload."""
    
    def __init__(self, registry: ContextRegistry):
        self.registry = registry

    async def resolve_all(self, request: Dict[str, Any]) -> List[ContextFragment]:
        fragments: List[ContextFragment] = []
        for name, provider in self.registry.providers.items():
            try:
                frags = await provider.provide_context(request)
                if frags:
                    fragments.extend(frags)
            except Exception as e:
                # Fault tolerant context resolution
                fragments.append(ContextFragment(
                    name=f"error_{name}",
                    content=f"[CONTEXT_PROVIDER_ERROR: {name}] {str(e)}",
                    priority=ContextPriority.METADATA,
                    source=name
                ))
        return fragments

class ContextRenderer:
    """Renders context envelope fragments into finalized system and user prompts for the LLM."""
    
    @staticmethod
    def render_envelope(envelope: ContextEnvelope) -> ContextEnvelope:
        envelope.sort_by_priority()
        
        system_frags = []
        user_frags = []

        for frag in envelope.fragments:
            if frag.priority in (ContextPriority.SYSTEM_PROMPT, ContextPriority.SAFETY_RULES, ContextPriority.DEVELOPER_INSTRUCTIONS):
                system_frags.append(frag.content)
            else:
                user_frags.append(frag.content)

        envelope.system_prompt = "\n\n".join(system_frags)
        envelope.user_prompt = "\n\n".join(user_frags)
        envelope.rendered_prompt = f"=== SYSTEM CONTEXT ===\n{envelope.system_prompt}\n\n=== USER CONTEXT ===\n{envelope.user_prompt}"
        return envelope

class ContextPipeline:
    """Configurable pipeline executing context providers, middleware filters, optimization, and rendering."""
    
    def __init__(self, registry: ContextRegistry, optimizer: Optional[IContextOptimizer] = None):
        self.registry = registry
        self.resolver = ContextResolver(registry)
        self.optimizer = optimizer or ContextOptimizer()

    async def execute(self, request: Dict[str, Any], max_token_budget: int = 4096) -> ContextEnvelope:
        req_id = request.get("request_id", f"req-{uuid.uuid4().hex[:6]}")
        envelope = ContextEnvelope(request_id=req_id, max_token_budget=max_token_budget)

        # 1. Resolve context fragments from providers
        fragments = await self.resolver.resolve_all(request)
        for f in fragments:
            envelope.add_fragment(f)

        # 2. Run Filter Middlewares
        for flt in self.registry.filters:
            envelope = await flt.filter(envelope)

        # 3. Optimize Token Budget
        envelope = await self.optimizer.optimize(envelope, max_tokens=max_token_budget)

        # 4. Run Transformer Middlewares
        for trf in self.registry.transformers:
            envelope = await trf.transform(envelope)

        # 5. Render Finalized Prompts
        envelope = ContextRenderer.render_envelope(envelope)
        return envelope

class ContextBuilder:
    """Fluent Builder for configuring system context, providers, and token budgets."""
    
    def __init__(self):
        self._system_prompt: str = "You are an Enterprise AI Agent operating under Clean Architecture."
        self._developer_instructions: str = ""
        self._max_token_budget: int = 4096
        self._custom_providers: List[IContextProvider] = []
        self._template_engine = PromptTemplateEngine()

    def with_system_prompt(self, prompt: str) -> 'ContextBuilder':
        self._system_prompt = prompt
        return self

    def with_system_prompt_file(self, filepath: str) -> 'ContextBuilder':
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self._system_prompt = f.read()
        return self

    def with_developer_instructions(self, instructions: str) -> 'ContextBuilder':
        self._developer_instructions = instructions
        return self

    def with_max_tokens(self, max_tokens: int) -> 'ContextBuilder':
        self._max_token_budget = max_tokens
        return self

    def with_provider(self, provider: IContextProvider) -> 'ContextBuilder':
        self._custom_providers.append(provider)
        return self

    def build(self) -> 'ContextEngine':
        registry = ContextRegistry()
        if self._system_prompt:
            registry.register_provider(SystemContextProvider(self._system_prompt))
        if self._developer_instructions:
            registry.register_provider(DeveloperContextProvider(self._developer_instructions))
        for p in self._custom_providers:
            registry.register_provider(p)

        return ContextEngine(
            registry=registry,
            template_engine=self._template_engine,
            max_token_budget=self._max_token_budget
        )

class ContextManager:
    """Manages active context state across chat sessions."""
    def __init__(self, engine: 'ContextEngine'):
        self.engine = engine
        self._session_contexts: Dict[str, List[ContextEnvelope]] = {}

    async def process_request(self, session_id: str, request_payload: Dict[str, Any]) -> ContextEnvelope:
        request_payload["session_id"] = session_id
        envelope = await self.engine.build_context(request_payload)
        if session_id not in self._session_contexts:
            self._session_contexts[session_id] = []
        self._session_contexts[session_id].append(envelope)
        return envelope

class ContextEngine:
    """Main Enterprise Context Engine for constructing, optimizing, validating, and managing all LLM context."""
    
    def __init__(
        self,
        registry: Optional[ContextRegistry] = None,
        template_engine: Optional[PromptTemplateEngine] = None,
        max_token_budget: int = 4096
    ):
        self.registry = registry or ContextRegistry()
        self.template_engine = template_engine or PromptTemplateEngine()
        self.token_manager = TokenBudgetManager(max_input_tokens=max_token_budget)
        self.pipeline = ContextPipeline(self.registry, optimizer=ContextOptimizer(self.token_manager))
        self.manager = ContextManager(self)

    @classmethod
    def builder(cls) -> ContextBuilder:
        return ContextBuilder()

    def register_provider(self, provider: IContextProvider):
        self.registry.register_provider(provider)

    async def build_context(self, request_payload: Dict[str, Any]) -> ContextEnvelope:
        """Constructs, optimizes, and renders the complete context envelope for a request."""
        return await self.pipeline.execute(request_payload, max_token_budget=self.token_manager.max_input_tokens)

    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        return self.template_engine.render(template_name, variables)
