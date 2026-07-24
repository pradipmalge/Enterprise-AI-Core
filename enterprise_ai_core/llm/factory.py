from typing import Optional
from enterprise_ai_core.llm.interfaces import ILLMProvider
from enterprise_ai_core.llm.gemini_provider import GeminiLLMProvider
from enterprise_ai_core.llm.openai_provider import OpenAIProvider, AzureOpenAIProvider

class LLMProviderFactory:
    @staticmethod
    def create_provider(provider_type: str = "gemini", **kwargs) -> ILLMProvider:
        provider_lower = provider_type.lower()
        if "gemini" in provider_lower:
            return GeminiLLMProvider(**kwargs)
        elif "azure" in provider_lower:
            return AzureOpenAIProvider(**kwargs)
        elif "openai" in provider_lower:
            return OpenAIProvider(**kwargs)
        else:
            return GeminiLLMProvider(**kwargs)
