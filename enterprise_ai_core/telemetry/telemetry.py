import time
from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class MetricPoint:
    name: str
    value: float
    tags: Dict[str, str]
    timestamp: float = field(default_factory=time.time)

class TelemetryCollector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelemetryCollector, cls).__new__(cls)
            cls._instance.metrics: List[MetricPoint] = []
            cls._instance.traces: List[Dict[str, Any]] = []
        return cls._instance

    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        point = MetricPoint(name=name, value=value, tags=tags or {})
        self.metrics.append(point)
        if len(self.metrics) > 1000:
            self.metrics.pop(0)

    def record_trace(self, trace_id: str, span_name: str, duration_ms: float, metadata: Dict[str, Any] = None):
        self.traces.append({
            "trace_id": trace_id,
            "span_name": span_name,
            "duration_ms": duration_ms,
            "metadata": metadata or {},
            "timestamp": time.time()
        })
        if len(self.traces) > 500:
            self.traces.pop(0)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_metrics_recorded": len(self.metrics),
            "total_traces_recorded": len(self.traces),
            "recent_traces": self.traces[-5:]
        }
