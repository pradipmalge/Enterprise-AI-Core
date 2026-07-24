export interface AgentStep {
  step_number: number;
  thought: string;
  action_tool: string;
  action_args?: Record<string, any>;
  observation: string;
}

export interface AgentResponse {
  success: boolean;
  response: string;
  agent_id: string;
  session_id: string;
  execution_time_ms: number;
  status: string;
  steps: AgentStep[];
  trace_logs: string[];
}

export interface FileNode {
  name: string;
  path: string;
  isDirectory: boolean;
  children?: FileNode[];
}

export interface MCPServerInfo {
  name: string;
  endpoint: string;
  status: string;
  tools: { name: string; description: string }[];
}

export interface ExampleMeta {
  id: string;
  number: string;
  title: string;
  description: string;
  path: string;
  category: string;
}

export interface TestResult {
  success: boolean;
  stdout: string;
  stderr: string;
  durationMs: number;
}
