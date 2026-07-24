import time
import json
from typing import Dict, Any, List, Optional
from enterprise_ai_core.common.result import Result

class EvaluationTestCase:
    def __init__(self, prompt: str, expected_keywords: List[str], max_latency_sec: float = 5.0):
        self.prompt = prompt
        self.expected_keywords = expected_keywords
        self.max_latency_sec = max_latency_sec

class EvaluationResult:
    def __init__(self, prompt: str, actual_response: str, latency_sec: float, score: float, passed: bool):
        self.prompt = prompt
        self.actual_response = actual_response
        self.latency_sec = latency_sec
        self.score = score
        self.passed = passed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "actual_response": self.actual_response,
            "latency_sec": round(self.latency_sec, 3),
            "score": round(self.score, 2),
            "passed": self.passed
        }

class AIEvaluationEngine:
    """Built-in AI Evaluation, Regression Testing & Benchmarking Framework."""

    def __init__(self, golden_dataset: Optional[List[EvaluationTestCase]] = None):
        self.dataset = golden_dataset or [
            EvaluationTestCase(
                prompt="What is SLA uptime guarantee?",
                expected_keywords=["99.9%", "SLA"],
                max_latency_sec=2.0
            )
        ]

    async def run_evaluation(self, agent: Any) -> Dict[str, Any]:
        results: List[EvaluationResult] = []
        total_score = 0.0

        for test in self.dataset:
            t0 = time.time()
            chat_res = await agent.chat(test.prompt)
            latency = time.time() - t0

            response_text = ""
            if chat_res.is_success and isinstance(chat_res.value, dict):
                response_text = chat_res.value.get("response", "")

            # Score keyword match
            matches = sum(1 for kw in test.expected_keywords if kw.lower() in response_text.lower())
            score = (matches / len(test.expected_keywords)) * 100 if test.expected_keywords else 100.0
            passed = score >= 50.0 and latency <= test.max_latency_sec

            results.append(EvaluationResult(test.prompt, response_text, latency, score, passed))
            total_score += score

        avg_score = total_score / len(self.dataset) if self.dataset else 100.0
        avg_latency = sum(r.latency_sec for r in results) / len(results) if results else 0.0

        return {
            "summary": {
                "total_tests": len(self.dataset),
                "passed_tests": sum(1 for r in results if r.passed),
                "average_score": round(avg_score, 2),
                "average_latency_sec": round(avg_latency, 3)
            },
            "test_reports": [r.to_dict() for r in results]
        }
