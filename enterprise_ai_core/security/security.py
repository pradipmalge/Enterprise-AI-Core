from typing import List, Dict, Any, Optional

class SecurityManager:
    def __init__(self, jwt_secret: str = "enterprise_secret_key"):
        self.jwt_secret = jwt_secret
        self.api_keys: Dict[str, str] = {"demo_key_123": "admin_tenant"}

    def validate_api_key(self, api_key: str) -> Optional[str]:
        return self.api_keys.get(api_key)

    def check_role_permission(self, user_roles: List[str], required_role: str) -> bool:
        return "admin" in user_roles or required_role in user_roles
