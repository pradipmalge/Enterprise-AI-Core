# LLM Module (`enterprise_ai_core.llm`)

The **LLM Module** provides unified driver abstractions for seamless integration with multiple LLM providers.

## Supported Providers

1. **GeminiProvider**: Driver for Google Gemini models (e.g. `gemini-3.6-flash`, `gemini-2.5-pro`).
2. **AzureOpenAIProvider**: Driver for Azure OpenAI deployments (e.g. `gpt-4o`, `gpt-4-turbo`).
3. **OpenAIProvider**: Driver for standard OpenAI API endpoints.
4. **OllamaProvider**: Driver for self-hosted local models via Ollama.
5. **AnthropicProvider**: Driver for Anthropic Claude models.

## Common Interface (`ILLMProvider`)

All provider drivers implement `ILLMProvider`:

```python
class ILLMProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> Result[str]:
        pass

    @abstractmethod
    async def generate_chat(self, messages: List[Dict[str, str]], **kwargs) -> Result[str]:
        pass
```

## Provider Fallback & Failover
LLM providers are registered into the `ModelRoutingEngine` for automatic priority-based failover and latency-aware routing.
