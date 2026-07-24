class FrameworkException(Exception):
    """Base exception for Enterprise AI Core framework."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

class AgentExecutionException(FrameworkException):
    def __init__(self, message: str, step: str = "unknown"):
        super().__init__(message, code="AGENT_EXECUTION_FAILED", details={"step": step})

class ToolExecutionException(FrameworkException):
    def __init__(self, tool_name: str, message: str):
        super().__init__(message, code="TOOL_EXECUTION_FAILED", details={"tool_name": tool_name})

class MCPException(FrameworkException):
    def __init__(self, message: str, server_name: str = "unknown"):
        super().__init__(message, code="MCP_ERROR", details={"server_name": server_name})

class LLMProviderException(FrameworkException):
    def __init__(self, provider: str, message: str):
        super().__init__(message, code="LLM_PROVIDER_ERROR", details={"provider": provider})

class DependencyInjectionException(FrameworkException):
    def __init__(self, service_type: str):
        super().__init__(f"Failed to resolve service type: {service_type}", code="DI_RESOLVE_FAILED")
