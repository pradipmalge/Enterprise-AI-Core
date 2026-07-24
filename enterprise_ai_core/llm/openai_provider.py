import os
import asyncio
from typing import AsyncGenerator, Dict, Any, List, Optional
from enterprise_ai_core.llm.interfaces import ILLMProvider
from enterprise_ai_core.common.result import Result

class OpenAIProvider(ILLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
    ) -> Result[Dict[str, Any]]:
        return Result.ok({
            "content": f"[OpenAI Provider - {self.model}] Processed: '{prompt}'",
            "model": self.model,
            "tool_calls": [],
            "finish_reason": "stop"
        })

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        yield f"[OpenAI Stream {self.model}] {prompt}"

class AzureOpenAIProvider(ILLMProvider):
    def __init__(self, endpoint: Optional[str] = None, api_key: Optional[str] = None, deployment_name: str = "gpt-4o-azure"):
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT", "https://demo.openai.azure.com/")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_KEY", "")
        self.deployment_name = deployment_name

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
    ) -> Result[Dict[str, Any]]:
        return Result.ok({
            "content": f"[Azure OpenAI Provider - Deployment: {self.deployment_name}] Response for query: '{prompt}'",
            "model": self.deployment_name,
            "tool_calls": [],
            "finish_reason": "stop"
        })

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        yield f"[Azure OpenAI Stream - {self.deployment_name}] Streaming output for '{prompt}'"
