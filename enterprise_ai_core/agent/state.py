from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AgentStep:
    step_number: int
    thought: str
    action_tool: str = ""
    action_args: Dict[str, Any] = field(default_factory=dict)
    observation: str = ""
    completed: bool = False

@dataclass
class AgentState:
    agent_id: str
    user_query: str
    steps: List[AgentStep] = field(default_factory=list)
    status: str = "INITIALIZED"  # INITIALIZED, PLANNING, EXECUTING, SUCCESS, FAILED
    final_answer: str = ""
    total_tokens: int = 0
