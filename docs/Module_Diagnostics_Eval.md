# Diagnostics & AI Evaluation Module (`enterprise_ai_core.diagnostics` & `enterprise_ai_core.eval`)

The **Diagnostics & AI Evaluation Module** provides system health monitoring, diagnostic checks, and automated AI model benchmarking.

## Diagnostics Engine (`enterprise_ai_core.diagnostics`)

Runs startup, dependency, environment, and health validation checks.

```python
from enterprise_ai_core import DiagnosticsEngine

report = DiagnosticsEngine.run_full_diagnostics()
print(f"System Health: {report.is_healthy}")
```

---

## AI Evaluation Framework (`enterprise_ai_core.eval`)

Executes golden dataset regression tests, measures token latencies, keyword accuracy scores, and generates performance reports.

```python
from enterprise_ai_core import AIEvaluationEngine, EvaluationTestCase

eval_engine = AIEvaluationEngine(golden_dataset=[
    EvaluationTestCase(prompt="What is our SLA guarantee?", expected_keywords=["99.9%"])
])

report = await eval_engine.run_evaluation(agent)
print(report["summary"])
```
