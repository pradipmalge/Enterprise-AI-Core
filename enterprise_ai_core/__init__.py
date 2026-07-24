"""
Enterprise AI Core Framework
An enterprise-grade Python framework for building AI Chatbots, AI Agents, Tool Calling, MCP Integration and AI Applications.
"""

from enterprise_ai_core.common.result import Result
from enterprise_ai_core.common.context import ExecutionContext, ConversationContext, RequestContext, ResponseContext
from enterprise_ai_core.common.di import ServiceCollection, DependencyContainer, ServiceProvider
from enterprise_ai_core.configuration.manager import ConfigurationManager
from enterprise_ai_core.agent.agent import EnterpriseAgent
from enterprise_ai_core.agent.builder import AgentBuilder
from enterprise_ai_core.tools.registry import ToolRegistry
from enterprise_ai_core.tools.decorators import tool
from enterprise_ai_core.mcp.client import MCPClient
from enterprise_ai_core.events.event_publisher import EventPublisher
from enterprise_ai_core.rag import (
    DocumentLoader,
    Document,
    RecursiveCharacterTextSplitter,
    VectorEmbeddingsProvider,
    VectorStore,
    extract_document_details,
    search_knowledge_base,
    ingest_document_to_rag,
)
from enterprise_ai_core.context import (
    ContextEngine,
    ContextBuilder,
    ContextPipeline,
    ContextManager,
    ContextRegistry,
    ContextResolver,
    ContextRenderer,
    ContextOptimizer,
    ContextCompressor,
    ContextSummarizer,
    TokenBudgetManager,
    PromptTemplateEngine,
    PromptRenderer,
    PromptCompiler,
    PromptValidator,
    PromptVersionManager,
    ContextPriority,
    ContextFragment,
    ContextEnvelope,
)
from enterprise_ai_core.guardrails import (
    GuardrailsEngine,
    GuardrailPipeline,
    GuardrailRegistry,
    GuardrailExecutor,
    GuardrailPolicy,
    GuardrailContext,
    GuardrailResult,
    ViolationReport,
    GuardrailConfiguration,
    GuardrailAction,
    GuardrailPhase,
    IGuardrail,
    IPreRequestGuardrail,
    IPrePromptGuardrail,
    IPostPromptGuardrail,
    IPreToolGuardrail,
    IPostToolGuardrail,
    IPostResponseGuardrail,
    PromptInjectionGuardrail,
    JailbreakGuardrail,
    PIIGuardrail,
    SecretsGuardrail,
    ToolPermissionGuardrail,
    RateLimitGuardrail,
    TokenBudgetGuardrail,
    ContentModerationGuardrail,
    JSONSchemaValidationGuardrail,
    HallucinationDetectionGuardrail,
    GuardrailPolicyEngine,
)

from enterprise_ai_core.routing.engine import ModelRoutingEngine
from enterprise_ai_core.policy.engine import AIPolicyEngine, AIPolicy
from enterprise_ai_core.features.manager import FeatureFlagsManager
from enterprise_ai_core.profiles.manager import EnvironmentProfileManager, EnvironmentType
from enterprise_ai_core.extension_sdk.sdk import FrameworkPlugin, PluginValidator
from enterprise_ai_core.lifecycle.events import LifecycleManager, LifecycleEvent
from enterprise_ai_core.eval.framework import AIEvaluationEngine
from enterprise_ai_core.diagnostics.engine import DiagnosticsEngine
from enterprise_ai_core.resiliency.circuit_breaker import CircuitBreaker, retry_with_backoff

__version__ = "1.0.0"

__all__ = [
    "EnterpriseAgent",
    "AgentBuilder",
    "ToolRegistry",
    "ServiceCollection",
    "DependencyContainer",
    "ServiceProvider",
    "ConfigurationManager",
    "ExecutionContext",
    "ConversationContext",
    "RequestContext",
    "ResponseContext",
    "Result",
    "EventPublisher",
    "MCPClient",
    "tool",
    "DocumentLoader",
    "Document",
    "RecursiveCharacterTextSplitter",
    "VectorEmbeddingsProvider",
    "VectorStore",
    "extract_document_details",
    "search_knowledge_base",
    "ingest_document_to_rag",
    # Context Engine
    "ContextEngine",
    "ContextBuilder",
    "ContextPipeline",
    "ContextManager",
    "ContextRegistry",
    "ContextResolver",
    "ContextRenderer",
    "ContextOptimizer",
    "ContextCompressor",
    "ContextSummarizer",
    "TokenBudgetManager",
    "PromptTemplateEngine",
    "PromptRenderer",
    "PromptCompiler",
    "PromptValidator",
    "PromptVersionManager",
    "ContextPriority",
    "ContextFragment",
    "ContextEnvelope",
    # Guardrails Engine
    "GuardrailsEngine",
    "GuardrailPipeline",
    "GuardrailRegistry",
    "GuardrailExecutor",
    "GuardrailPolicy",
    "GuardrailContext",
    "GuardrailResult",
    "ViolationReport",
    "GuardrailConfiguration",
    "GuardrailAction",
    "GuardrailPhase",
    "IGuardrail",
    "IPreRequestGuardrail",
    "IPrePromptGuardrail",
    "IPostPromptGuardrail",
    "IPreToolGuardrail",
    "IPostToolGuardrail",
    "IPostResponseGuardrail",
    "PromptInjectionGuardrail",
    "JailbreakGuardrail",
    "PIIGuardrail",
    "SecretsGuardrail",
    "ToolPermissionGuardrail",
    "RateLimitGuardrail",
    "TokenBudgetGuardrail",
    "ContentModerationGuardrail",
    "JSONSchemaValidationGuardrail",
    "HallucinationDetectionGuardrail",
    "GuardrailPolicyEngine",
    # Enterprise Additions
    "ModelRoutingEngine",
    "AIPolicyEngine",
    "AIPolicy",
    "FeatureFlagsManager",
    "EnvironmentProfileManager",
    "EnvironmentType",
    "FrameworkPlugin",
    "PluginValidator",
    "LifecycleManager",
    "LifecycleEvent",
    "AIEvaluationEngine",
    "DiagnosticsEngine",
    "CircuitBreaker",
    "retry_with_backoff"
]

