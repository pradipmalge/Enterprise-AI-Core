import inspect
import asyncio
from typing import Callable, Any, Dict, Optional, Type
from enterprise_ai_core.tools.interfaces import ITool, ToolMetadata
from enterprise_ai_core.common.result import Result

def tool(name: Optional[str] = None, description: Optional[str] = None):
    """Decorator to transform a Python function or class into an ITool."""
    def decorator(obj: Any):
        tool_name = name or (obj.__name__ if hasattr(obj, '__name__') else obj.__class__.__name__)
        docstring = description or (inspect.getdoc(obj) or f"Tool {tool_name}")

        # Extract parameters schema
        sig = inspect.signature(obj if inspect.isfunction(obj) else obj.__call__)
        props = {}
        required = []
        for param_name, param in sig.parameters.items():
            if param_name in ('self', 'cls'):
                continue
            param_type = "string"
            if param.annotation == int or param.annotation == float:
                param_type = "number"
            elif param.annotation == bool:
                param_type = "boolean"
            elif param.annotation == dict:
                param_type = "object"
            elif param.annotation == list:
                param_type = "array"

            props[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}"
            }
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        meta = ToolMetadata(
            name=tool_name,
            description=docstring,
            parameters={"type": "object", "properties": props},
            required=required
        )

        class FunctionalTool(ITool):
            @property
            def metadata(self) -> ToolMetadata:
                return meta

            def __call__(self, *args, **kwargs) -> Any:
                target = obj if inspect.isfunction(obj) else (obj() if inspect.isclass(obj) else obj)
                func = target if inspect.isfunction(target) else getattr(target, '__call__', None) or target.execute
                return func(*args, **kwargs)

            async def execute(self, **kwargs) -> Result[Any]:
                try:
                    target = obj if inspect.isfunction(obj) else (obj() if inspect.isclass(obj) else obj)
                    func = target if inspect.isfunction(target) else getattr(target, '__call__', None) or target.execute
                    if asyncio.iscoroutinefunction(func):
                        res = await func(**kwargs)
                    else:
                        res = func(**kwargs)
                    return Result.ok(res)
                except Exception as ex:
                    return Result.fail(f"Tool execution failed: {str(ex)}")

        return FunctionalTool()
    return decorator
