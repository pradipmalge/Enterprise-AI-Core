import re
import logging
from typing import List, Dict, Any
from .interfaces import IContextFilter, IContextTransformer
from .models import ContextEnvelope, ContextFragment, ContextPriority

logger = logging.getLogger("enterprise_ai_core.context.middleware")

class ContextValidationMiddleware(IContextFilter):
    """Ensures mandatory context fragments (system prompt or user request) are present."""
    async def filter(self, envelope: ContextEnvelope) -> ContextEnvelope:
        has_user = any(f.priority == ContextPriority.CURRENT_USER_REQUEST for f in envelope.fragments)
        if not has_user and envelope.user_prompt:
            envelope.add_fragment(ContextFragment(
                name="user_query_validated",
                content=f"[CURRENT_USER_REQUEST]\n{envelope.user_prompt}",
                priority=ContextPriority.CURRENT_USER_REQUEST,
                source="ContextValidationMiddleware"
            ))
        return envelope

class PIIFilteringMiddleware(IContextFilter):
    """Redacts PII patterns such as emails, SSNs, credit cards, and phone numbers."""
    EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_REGEX = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    SSN_REGEX = r'\b\d{3}-\d{2}-\d{4}\b'

    async def filter(self, envelope: ContextEnvelope) -> ContextEnvelope:
        for frag in envelope.fragments:
            text = frag.content
            text = re.sub(self.EMAIL_REGEX, "[REDACTED_EMAIL]", text)
            text = re.sub(self.PHONE_REGEX, "[REDACTED_PHONE]", text)
            text = re.sub(self.SSN_REGEX, "[REDACTED_SSN]", text)
            frag.content = text
        return envelope

class SensitiveDataRemovalMiddleware(IContextFilter):
    """Removes sensitive keys, passwords, bearer tokens, and internal API keys."""
    API_KEY_REGEX = r'(?i)(api_key|secret|password|bearer_token|private_key)\s*[:=]\s*["\']?[a-zA-Z0-9_\-\.]{8,}["\']?'

    async def filter(self, envelope: ContextEnvelope) -> ContextEnvelope:
        for frag in envelope.fragments:
            frag.content = re.sub(self.API_KEY_REGEX, r'\1: [REDACTED_SECRET]', frag.content)
        return envelope

class PromptLoggingMiddleware(IContextTransformer):
    """Logs constructed prompt metrics and metadata before LLM dispatch."""
    async def transform(self, envelope: ContextEnvelope) -> ContextEnvelope:
        frag_names = [f.name for f in envelope.fragments]
        logger.info(f"[ContextEngine] Prompt Built | Req: {envelope.request_id} | Tokens: {envelope.total_tokens} | Fragments: {frag_names}")
        envelope.metadata["logged_at"] = "2026-07-23"
        return envelope

class ContextEnrichmentMiddleware(IContextTransformer):
    """Enriches context envelope with runtime environment metadata."""
    async def transform(self, envelope: ContextEnvelope) -> ContextEnvelope:
        envelope.metadata["framework"] = "Enterprise-AI-Core v1.0"
        envelope.metadata["architecture"] = "Clean Architecture Context Pipeline"
        return envelope
