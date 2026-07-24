from typing import List, Dict, Any
from .models import ContextEnvelope, ContextFragment, ContextPriority
from .interfaces import IContextOptimizer

class TokenBudgetManager:
    """Enterprise Token Budget Manager for estimating, reserving, and optimizing token usage."""
    
    def __init__(self, max_input_tokens: int = 4096, reserve_response_tokens: int = 1024):
        self.max_input_tokens = max_input_tokens
        self.reserve_response_tokens = reserve_response_tokens
        self.effective_input_budget = max(512, max_input_tokens - reserve_response_tokens)

    def estimate_tokens(self, text: str) -> int:
        """Estimates token count (~4 characters per token)."""
        return max(1, len(text) // 4)

    def check_budget(self, envelope: ContextEnvelope) -> bool:
        total = envelope.calculate_total_tokens()
        return total <= self.effective_input_budget

class ContextCompressor:
    """Compresses lengthy context text without breaking semantic keywords."""
    @staticmethod
    def compress_text(text: str, max_words: int = 100) -> str:
        words = text.split()
        if len(words) <= max_words:
            return text
        half = max_words // 2
        compressed = " ".join(words[:half]) + f" ... [COMPRESSED {len(words) - max_words} WORDS] ... " + " ".join(words[-half:])
        return compressed

class ContextSummarizer:
    """Summarizes conversation or knowledge chunks for token efficiency."""
    @staticmethod
    def summarize_fragment(fragment: ContextFragment) -> ContextFragment:
        compressed_text = ContextCompressor.compress_text(fragment.content, max_words=60)
        return ContextFragment(
            name=f"{fragment.name}_summarized",
            content=f"[SUMMARIZED_CONTEXT: {fragment.name}]\n{compressed_text}",
            priority=fragment.priority,
            source=f"{fragment.source}_summarizer"
        )

class ContextOptimizer(IContextOptimizer):
    """Enforces strict priority-based token budgeting on context envelopes."""
    
    def __init__(self, token_manager: TokenBudgetManager = None):
        self.token_manager = token_manager or TokenBudgetManager()

    async def optimize(self, envelope: ContextEnvelope, max_tokens: int = 4096) -> ContextEnvelope:
        effective_budget = max(512, max_tokens - self.token_manager.reserve_response_tokens)
        envelope.sort_by_priority()
        
        current_tokens = envelope.calculate_total_tokens()
        if current_tokens <= effective_budget:
            return envelope

        # Token overflow detected: trim or drop lowest priority fragments (Priority 9 down to 5)
        optimized_fragments: List[ContextFragment] = []

        for fragment in envelope.fragments:
            # High Priority items (Priority 1: System, 2: Safety, 3: Developer, 4: Current User Query) are preserved
            if fragment.priority <= ContextPriority.CURRENT_USER_REQUEST:
                optimized_fragments.append(fragment)
                continue

            # Medium Priority items (Conversation, RAG) are summarized if over budget
            frag_tokens = fragment.tokens_estimated
            projected = sum(f.tokens_estimated for f in optimized_fragments) + frag_tokens

            if projected <= effective_budget:
                optimized_fragments.append(fragment)
            else:
                # Try compressing/summarizing fragment
                summarized = ContextSummarizer.summarize_fragment(fragment)
                if sum(f.tokens_estimated for f in optimized_fragments) + summarized.tokens_estimated <= effective_budget:
                    optimized_fragments.append(summarized)
                    envelope.compressed = True
                else:
                    envelope.dropped_fragments.append(fragment.name)

        envelope.fragments = optimized_fragments
        envelope.calculate_total_tokens()
        return envelope
