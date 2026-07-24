import os
import re
import json
try:
    import yaml
except ImportError:
    yaml = None
from typing import Dict, Any, Optional, List

class PromptTemplate:
    def __init__(self, name: str, template: str, version: str = "v1.0", metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.template = template
        self.version = version
        self.metadata = metadata or {}
        self.required_vars = self._extract_vars(template)

    def _extract_vars(self, template: str) -> List[str]:
        return list(set(re.findall(r'\{\{\s*([a-zA-Z0-9_]+)\s*\}\}', template)))

    def render(self, variables: Dict[str, Any]) -> str:
        rendered = self.template
        for var in self.required_vars:
            val = variables.get(var, f"[{var}]")
            rendered = re.sub(r'\{\{\s*' + re.escape(var) + r'\s*\}\}', str(val), rendered)
        return rendered

class PromptValidator:
    @staticmethod
    def validate(template: PromptTemplate, variables: Dict[str, Any]) -> List[str]:
        missing = []
        for var in template.required_vars:
            if var not in variables:
                missing.append(var)
        return missing

class PromptCompiler:
    @staticmethod
    def compile(template: PromptTemplate):
        def compiled_fn(vars_dict: Dict[str, Any]) -> str:
            return template.render(vars_dict)
        return compiled_fn

class PromptVersionManager:
    def __init__(self):
        self._templates: Dict[str, Dict[str, PromptTemplate]] = {}

    def register(self, template: PromptTemplate):
        if template.name not in self._templates:
            self._templates[template.name] = {}
        self._templates[template.name][template.version] = template

    def get(self, name: str, version: str = "v1.0") -> Optional[PromptTemplate]:
        return self._templates.get(name, {}).get(version)

    def list_versions(self, name: str) -> List[str]:
        return list(self._templates.get(name, {}).keys())

class PromptTemplateEngine:
    """Enterprise Prompt Template Engine for loading, compiling, and rendering versioned prompts."""
    
    def __init__(self, prompt_dir: str = "prompts"):
        self.prompt_dir = prompt_dir
        self.version_manager = PromptVersionManager()
        self._load_default_templates()

    def _load_default_templates(self):
        # Register standard built-in prompt templates
        defaults = {
            "system.md": "You are {{ agent_name }}, an Enterprise AI operating under {{ architecture_style }}.",
            "assistant.md": "Assistant Context: {{ context_description }}.",
            "planner.md": "Create an execution plan for query: '{{ query }}'. Available tools: {{ tools }}.",
            "reviewer.md": "Review output '{{ output }}' against security policy {{ policy }}.",
            "tool_selector.md": "Select optimal tool for goal '{{ goal }}'. Options: {{ available_tools }}.",
            "reflection.md": "Reflect on step {{ step_num }} result: {{ result }}.",
            "summarizer.md": "Summarize conversation history: {{ history_text }}.",
            "memory.md": "Recalled memories for user {{ user_id }}: {{ memory_facts }}.",
            "rag.md": "Given knowledge chunks: {{ knowledge_chunks }}, answer prompt: {{ prompt }}.",
            "safety.md": "Ensure output complies with rules: {{ safety_rules }}.",
            "code_generator.md": "Generate {{ language }} code for architecture spec: {{ spec }}."
        }

        for fname, tmpl_str in defaults.items():
            name = fname.replace(".md", "")
            self.version_manager.register(PromptTemplate(name=name, template=tmpl_str, version="v1.0"))

        # Load file-based prompts if directory exists
        if os.path.exists(self.prompt_dir):
            for f in os.listdir(self.prompt_dir):
                fpath = os.path.join(self.prompt_dir, f)
                if f.endswith(".md"):
                    with open(fpath, "r", encoding="utf-8") as file:
                        content = file.read()
                        name = f.replace(".md", "")
                        self.version_manager.register(PromptTemplate(name=name, template=content, version="v1.0"))

    def render(self, template_name: str, variables: Dict[str, Any], version: str = "v1.0") -> str:
        tmpl = self.version_manager.get(template_name, version)
        if not tmpl:
            return f"[TEMPLATE NOT FOUND: {template_name}]"
        
        missing = PromptValidator.validate(tmpl, variables)
        if missing:
            # Inject defaults for missing
            for m in missing:
                variables[m] = f"[{m}]"
        
        return tmpl.render(variables)

class PromptRenderer:
    def __init__(self, engine: PromptTemplateEngine):
        self.engine = engine

    def render_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        return self.engine.render(template_name, variables)
