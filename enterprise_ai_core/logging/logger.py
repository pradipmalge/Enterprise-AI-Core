import logging
import json
import sys
from typing import Any, Optional, Dict
from enterprise_ai_core.logging.interfaces import ILogger

class StructuredLogger(ILogger):
    def __init__(self, name: str = "EnterpriseAICore"):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _format_meta(self, context: Optional[Dict[str, Any]]) -> str:
        if not context:
            return ""
        try:
            return f" | Context: {json.dumps(context)}"
        except Exception:
            return f" | Context: {str(context)}"

    def info(self, msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.logger.info(f"{msg}{self._format_meta(context)}")

    def warning(self, msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.logger.warning(f"{msg}{self._format_meta(context)}")

    def error(self, msg: str, exc: Optional[Exception] = None, context: Optional[Dict[str, Any]] = None) -> None:
        if exc:
            self.logger.error(f"{msg} - Exception: {str(exc)}{self._format_meta(context)}", exc_info=True)
        else:
            self.logger.error(f"{msg}{self._format_meta(context)}")

    def debug(self, msg: str, context: Optional[Dict[str, Any]] = None) -> None:
        self.logger.debug(f"{msg}{self._format_meta(context)}")
