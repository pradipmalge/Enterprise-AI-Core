from typing import List, Dict, Any
from enterprise_ai_core.agent.state import AgentStep, AgentState
from enterprise_ai_core.tools.registry import ToolRegistry

class ExecutionPlanner:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def create_plan(self, query: str) -> List[AgentStep]:
        # Intelligent heuristic tool match for query
        available_tools = self.tool_registry.list_tools()
        steps = []
        q_lower = query.lower()

        # Step 1: Tool search matching query
        selected_tool = None
        for t in available_tools:
            name = t.metadata.name.lower()
            if any(k in q_lower for k in name.split("_")):
                selected_tool = t
                break

        if selected_tool:
            steps.append(AgentStep(
                step_number=1,
                thought=f"Query requires tool '{selected_tool.metadata.name}' to retrieve domain information.",
                action_tool=selected_tool.metadata.name,
                action_args={"query": query}
            ))
            steps.append(AgentStep(
                step_number=2,
                thought="Synthesize observation into final comprehensive response.",
                action_tool="",
                completed=False
            ))
        else:
            steps.append(AgentStep(
                step_number=1,
                thought="Direct reasoning & synthesis without external tool execution.",
                action_tool="",
                completed=False
            ))

        return steps
