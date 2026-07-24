import os
from typing import Any, Optional, Dict
from enterprise_ai_core.configuration.interfaces import IConfiguration

class ConfigurationManager(IConfiguration):
    def __init__(self, initial_config: Optional[Dict[str, Any]] = None):
        self._config: Dict[str, Any] = {
            "app_name": "Enterprise AI App",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "llm_provider": os.getenv("LLM_PROVIDER", "gemini"),
            "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            "kafka_bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            "rabbitmq_url": os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
            "max_retry_attempts": int(os.getenv("MAX_RETRY_ATTEMPTS", "3")),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        }
        if initial_config:
            self._config.update(initial_config)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        # Check environment variable overriding (UPPER_CASE)
        env_key = key.upper()
        if env_key in os.environ:
            return os.environ[env_key]
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return self._config.copy()
