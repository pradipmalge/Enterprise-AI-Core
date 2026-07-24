from typing import Dict, Any, Type, Callable, Optional
import inspect
from enterprise_ai_core.common.exceptions import DependencyInjectionException

class ServiceDescriptor:
    def __init__(self, service_type: Any, implementation: Any, lifetime: str = "singleton"):
        self.service_type = service_type
        self.implementation = implementation
        self.lifetime = lifetime  # "singleton" or "transient"
        self.instance: Optional[Any] = None

class ServiceProvider:
    def __init__(self, descriptors: Dict[Any, ServiceDescriptor]):
        self._descriptors = descriptors

    def get_service(self, service_type: Any) -> Any:
        descriptor = self._descriptors.get(service_type)
        if not descriptor:
            # If instance itself was passed or registered directly
            for key, desc in self._descriptors.items():
                if isinstance(key, str) and key == str(service_type):
                    descriptor = desc
                    break
        if not descriptor:
            raise DependencyInjectionException(str(service_type))

        if descriptor.lifetime == "singleton":
            if descriptor.instance is None:
                descriptor.instance = self._instantiate(descriptor.implementation)
            return descriptor.instance
        else:
            return self._instantiate(descriptor.implementation)

    def _instantiate(self, impl: Any) -> Any:
        if callable(impl) and not inspect.isclass(impl):
            return impl(self)
        if inspect.isclass(impl):
            # Resolve constructor dependencies
            sig = inspect.signature(impl.__init__)
            params = {}
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                if param.annotation != inspect.Parameter.empty:
                    try:
                        params[param_name] = self.get_service(param.annotation)
                    except DependencyInjectionException:
                        if param.default != inspect.Parameter.empty:
                            params[param_name] = param.default
            return impl(**params)
        return impl

class ServiceCollection:
    def __init__(self):
        self._descriptors: Dict[Any, ServiceDescriptor] = {}

    def add_singleton(self, service_type: Any, implementation: Any) -> 'ServiceCollection':
        self._descriptors[service_type] = ServiceDescriptor(service_type, implementation, lifetime="singleton")
        return self

    def add_transient(self, service_type: Any, implementation: Any) -> 'ServiceCollection':
        self._descriptors[service_type] = ServiceDescriptor(service_type, implementation, lifetime="transient")
        return self

    def build_service_provider(self) -> ServiceProvider:
        return ServiceProvider(self._descriptors)

class DependencyContainer:
    """Global wrapper for IoC container management."""
    _instance: Optional[ServiceProvider] = None

    @classmethod
    def set_provider(cls, provider: ServiceProvider):
        cls._instance = provider

    @classmethod
    def get_service(cls, service_type: Any) -> Any:
        if not cls._instance:
            raise DependencyInjectionException("Container not built.")
        return cls._instance.get_service(service_type)
