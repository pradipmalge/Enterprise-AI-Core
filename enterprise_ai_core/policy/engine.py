import json
from typing import Dict, Any, List, Optional
from enterprise_ai_core.common.result import Result

try:
    import yaml
except ImportError:
    yaml = None

class AIPolicy:
    def __init__(
        self,
        allowed_models: Optional[List[str]] = None,
        allowed_tools: Optional[List[str]] = None,
        allowed_mcp_servers: Optional[List[str]] = None,
        allowed_plugins: Optional[List[str]] = None,
        max_prompt_tokens: int = 8000,
        max_response_tokens: int = 2000,
        max_execution_time_sec: float = 60.0,
        role_policies: Optional[Dict[str, Any]] = None,
        department_policies: Optional[Dict[str, Any]] = None,
        user_policies: Optional[Dict[str, Any]] = None
    ):
        self.allowed_models = allowed_models
        self.allowed_tools = allowed_tools
        self.allowed_mcp_servers = allowed_mcp_servers
        self.allowed_plugins = allowed_plugins
        self.max_prompt_tokens = max_prompt_tokens
        self.max_response_tokens = max_response_tokens
        self.max_execution_time_sec = max_execution_time_sec
        self.role_policies = role_policies or {}
        self.department_policies = department_policies or {}
        self.user_policies = user_policies or {}

class AIPolicyEngine:
    """Centralized AI Governance and Policy Engine."""

    def __init__(self, global_policy: Optional[AIPolicy] = None):
        self.global_policy = global_policy or AIPolicy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIPolicyEngine':
        pol_dict = data.get("policy", data)
        policy = AIPolicy(
            allowed_models=pol_dict.get("allowed_models"),
            allowed_tools=pol_dict.get("allowed_tools"),
            allowed_mcp_servers=pol_dict.get("allowed_mcp_servers"),
            allowed_plugins=pol_dict.get("allowed_plugins"),
            max_prompt_tokens=pol_dict.get("max_prompt_tokens", 8000),
            max_response_tokens=pol_dict.get("max_response_tokens", 2000),
            max_execution_time_sec=pol_dict.get("max_execution_time_sec", 60.0),
            role_policies=pol_dict.get("role_policies", {}),
            department_policies=pol_dict.get("department_policies", {}),
            user_policies=pol_dict.get("user_policies", {})
        )
        return cls(global_policy=policy)

    @classmethod
    def from_yaml(cls, yaml_content: str) -> 'AIPolicyEngine':
        if yaml is None:
            data = json.loads(yaml_content)
        else:
            data = yaml.safe_load(yaml_content)
        return cls.from_dict(data)

    def validate_tool_access(self, tool_name: str, user_role: str = "user") -> Result[bool]:
        if self.global_policy.allowed_tools is not None:
            if tool_name not in self.global_policy.allowed_tools:
                return Result.fail(f"Tool '{tool_name}' is not authorized under AI Policy.")
        
        if user_role in self.global_policy.role_policies:
            role_allowed_tools = self.global_policy.role_policies[user_role].get("allowed_tools")
            if role_allowed_tools is not None and tool_name not in role_allowed_tools:
                return Result.fail(f"Tool '{tool_name}' forbidden for role '{user_role}'.")

        return Result.ok(True)

    def validate_model_access(self, model_name: str) -> Result[bool]:
        if self.global_policy.allowed_models is not None:
            if model_name not in self.global_policy.allowed_models:
                return Result.fail(f"Model '{model_name}' is not in the allowed model registry.")
        return Result.ok(True)
