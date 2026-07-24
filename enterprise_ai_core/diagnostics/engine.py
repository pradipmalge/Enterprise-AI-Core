import sys
import importlib
from typing import Dict, Any, List

class DiagnosticsReport:
    def __init__(self, is_healthy: bool, checks: List[Dict[str, Any]], recommendations: List[str]):
        self.is_healthy = is_healthy
        self.checks = checks
        self.recommendations = recommendations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "healthy": self.is_healthy,
            "checks": self.checks,
            "recommendations": self.recommendations
        }

class DiagnosticsEngine:
    """Enterprise framework diagnostics and system health inspection."""

    @staticmethod
    def run_full_diagnostics() -> DiagnosticsReport:
        checks = []
        recommendations = []
        healthy = True

        # Check 1: Python Version
        py_ver = sys.version_info
        if py_ver.major >= 3 and py_ver.minor >= 9:
            checks.append({"name": "Python Runtime", "status": "PASS", "details": f"Python {py_ver.major}.{py_ver.minor}"})
        else:
            checks.append({"name": "Python Runtime", "status": "WARN", "details": f"Python {py_ver.major}.{py_ver.minor} (Recommend Python 3.10+)"})

        # Check 2: Core Dependencies
        core_deps = ["json", "asyncio", "sys", "os"]
        for dep in core_deps:
            try:
                importlib.import_module(dep)
                checks.append({"name": f"Dependency: {dep}", "status": "PASS", "details": "Installed"})
            except ImportError:
                checks.append({"name": f"Dependency: {dep}", "status": "FAIL", "details": "Missing"})
                healthy = False
                recommendations.append(f"Install missing dependency '{dep}' via pip.")

        # Check 3: Optional Libraries
        for opt_dep in ["pydantic", "yaml"]:
            try:
                importlib.import_module(opt_dep)
                checks.append({"name": f"Optional Dependency: {opt_dep}", "status": "PASS", "details": "Installed"})
            except ImportError:
                checks.append({"name": f"Optional Dependency: {opt_dep}", "status": "INFO", "details": f"Missing (Optional extension component)"})


        return DiagnosticsReport(is_healthy=healthy, checks=checks, recommendations=recommendations)
