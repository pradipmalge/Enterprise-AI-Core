from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class FrameworkPlugin(ABC):
    """Base class for writing custom framework plugins and extensions."""

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @abstractmethod
    def initialize(self, container: Any) -> bool:
        """Initialize the extension into the DI container or agent context."""
        pass

class PluginValidator:
    """Validates third-party framework plugins for compatibility."""

    @staticmethod
    def validate_plugin(plugin: FrameworkPlugin) -> bool:
        if not hasattr(plugin, "plugin_name") or not plugin.plugin_name:
            raise ValueError("Plugin missing valid 'plugin_name'")
        if not hasattr(plugin, "version") or not plugin.version:
            raise ValueError("Plugin missing valid 'version'")
        return True
