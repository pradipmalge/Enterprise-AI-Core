from typing import Dict, Any, Type
from enterprise_ai_core.common.result import Result

class PluginLoader:
    def __init__(self):
        self._plugins: Dict[str, Any] = {}

    def register_plugin(self, name: str, plugin_instance: Any):
        self._plugins[name] = plugin_instance

    def get_plugin(self, name: str) -> Any:
        return self._plugins.get(name)

    def list_plugins(self) -> Dict[str, Any]:
        return self._plugins.copy()
