# Prompt Templates & Prompt Rendering

The `enterprise_ai_core/context/templates.py` package manages prompt templates, version control, and template rendering.

```mermaid
graph LR
    A[Template File (.md)] --> B[PromptTemplateEngine]
    B --> C[PromptVersionManager]
    C --> D[PromptCompiler]
    D --> E[PromptValidator]
    E --> F[Rendered Prompt String]
```

## Built-in Templates (`prompts/`)

- `prompts/system.md`
- `prompts/assistant.md`
- `prompts/planner.md`
- `prompts/reviewer.md`
- `prompts/tool_selector.md`
- `prompts/reflection.md`
- `prompts/summarizer.md`
- `prompts/memory.md`
- `prompts/rag.md`
- `prompts/safety.md`
- `prompts/code_generator.md`

## Variable Substitution Example

```python
from enterprise_ai_core.context import PromptTemplateEngine

engine = PromptTemplateEngine()
prompt = engine.render("planner", {
    "query": "Generate Q3 Financial Report",
    "tools": ["excel_parser", "pdf_generator"]
})
print(prompt)
```
