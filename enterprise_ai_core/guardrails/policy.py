import json
from typing import Dict, Any, Union, Optional
from .models import GuardrailPolicy, GuardrailConfiguration

try:
    import yaml
except ImportError:
    yaml = None

class GuardrailPolicyEngine:
    """Parses and manages Guardrail policies from Python dicts, JSON strings, or YAML configs."""

    @staticmethod
    def load_from_dict(config_dict: Dict[str, Any]) -> GuardrailPolicy:
        policy_data = config_dict.get("policies", config_dict.get("policy", config_dict))
        
        return GuardrailPolicy(
            allow_tools=policy_data.get("allow_tools"),
            deny_tools=policy_data.get("deny_tools", []),
            max_prompt_tokens=policy_data.get("max_prompt_tokens", 8000),
            max_response_tokens=policy_data.get("max_response_tokens", 2000),
            allowed_roles=policy_data.get("allowed_roles"),
            enable_pii_redaction=policy_data.get("enable_pii_redaction", True),
            enable_prompt_injection_check=policy_data.get("enable_prompt_injection_check", True),
            enable_secrets_detection=policy_data.get("enable_secrets_detection", True),
            custom_rules=policy_data.get("custom_rules", {})
        )

    @staticmethod
    def load_from_json(json_str: str) -> GuardrailPolicy:
        data = json.loads(json_str)
        return GuardrailPolicyEngine.load_from_dict(data)

    @staticmethod
    def load_from_yaml(yaml_str: str) -> GuardrailPolicy:
        if yaml is None:
            # Fallback to json if yaml library isn't available
            data = json.loads(yaml_str)
        else:
            data = yaml.safe_load(yaml_str)
        return GuardrailPolicyEngine.load_from_dict(data)
