from typing import Dict, Any, Optional

class FeatureFlagsManager:
    """Runtime Feature Flags Manager for Enterprise AI Core."""

    def __init__(self, overrides: Optional[Dict[str, bool]] = None):
        self._flags: Dict[str, bool] = {
            "EnableRAG": True,
            "EnableMemory": True,
            "EnableRedis": False,
            "EnableKafka": False,
            "EnableStreaming": True,
            "EnableGuardrails": True,
            "EnableMCP": True,
            "EnableWorkflow": True,
            "EnableTelemetry": True,
            "EnableAudit": True,
        }
        if overrides:
            self._flags.update(overrides)

    def is_enabled(self, feature_name: str) -> bool:
        return self._flags.get(feature_name, True)

    def set_flag(self, feature_name: str, enabled: bool):
        self._flags[feature_name] = enabled

    def get_all_flags(self) -> Dict[str, bool]:
        return self._flags.copy()
