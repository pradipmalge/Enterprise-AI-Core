from enum import Enum
from typing import Dict, Any, Optional

class EnvironmentType(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    QA = "QA"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

class EnvironmentProfile:
    def __init__(
        self,
        env_type: EnvironmentType = EnvironmentType.DEVELOPMENT,
        model_name: str = "gemini-3.6-flash",
        log_level: str = "INFO",
        fail_fast_guardrails: bool = True,
        enable_telemetry: bool = True,
        max_prompt_tokens: int = 8000
    ):
        self.env_type = env_type
        self.model_name = model_name
        self.log_level = log_level
        self.fail_fast_guardrails = fail_fast_guardrails
        self.enable_telemetry = enable_telemetry
        self.max_prompt_tokens = max_prompt_tokens

class EnvironmentProfileManager:
    """Manages profile configurations across environments."""

    DEFAULT_PROFILES = {
        EnvironmentType.DEVELOPMENT: EnvironmentProfile(
            env_type=EnvironmentType.DEVELOPMENT,
            model_name="gemini-3.6-flash",
            log_level="DEBUG",
            fail_fast_guardrails=False,
            enable_telemetry=False,
            max_prompt_tokens=4000
        ),
        EnvironmentType.PRODUCTION: EnvironmentProfile(
            env_type=EnvironmentType.PRODUCTION,
            model_name="gemini-3.6-flash",
            log_level="WARN",
            fail_fast_guardrails=True,
            enable_telemetry=True,
            max_prompt_tokens=16000
        )
    }

    def __init__(self, current_env: EnvironmentType = EnvironmentType.DEVELOPMENT):
        self.current_env = current_env
        self._profiles = self.DEFAULT_PROFILES.copy()

    def get_profile(self) -> EnvironmentProfile:
        return self._profiles.get(self.current_env, self.DEFAULT_PROFILES[EnvironmentType.DEVELOPMENT])
