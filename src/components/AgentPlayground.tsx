import React, { useState } from 'react';
import { Send, Bot, Database, Zap, Clock, ShieldCheck, Layers, Play, CheckCircle2, ChevronRight, Copy, Check } from 'lucide-react';
import { AgentResponse } from '../types';

export const AgentPlayground: React.FC = () => {
  const [query, setQuery] = useState("Find customer 101 and summarize their last three orders.");
  const [llmProvider, setLlmProvider] = useState("gemini");
  const [useMemoryCache, setUseMemoryCache] = useState(true);
  const [useEventBus, setUseEventBus] = useState(true);
  const [mcpEnabled, setMcpEnabled] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AgentResponse | null>(null);
  const [copied, setCopied] = useState(false);

  const handleRunAgent = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/agent/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          provider: llmProvider,
          useCache: useMemoryCache,
          useBus: useEventBus,
          useMcp: mcpEnabled,
        }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generatedBuilderCode = `from enterprise_ai_core import EnterpriseAgent, tool

@tool(name="customer_search", description="Search customer CRM")
def customer_search(customer_id: str) -> str:
    return f"Customer {customer_id}: Acme Corp, Tier=Enterprise Gold"

agent = (
    EnterpriseAgent.builder()
        .${llmProvider === 'azure' ? 'use_azure_openai()' : llmProvider === 'openai' ? 'use_openai()' : 'use_gemini()'}
        ${useMemoryCache ? '.use_memory_cache()' : ''}
        ${useEventBus ? '.use_in_memory_bus()' : ''}
        .register_tool(customer_search)
        ${mcpEnabled ? '.discover_mcp_servers()' : ''}
        .build()
)

response = await agent.chat("${query.replace(/"/g, '\\"')}")
print(response.value["response"])`;

  const handleCopyCode = () => {
    navigator.clipboard.writeText(generatedBuilderCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Grid Container */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column - Builder Configuration */}
        <div className="lg:col-span-4 border-2 border-[#141414] bg-white/40 p-5 space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            <h2 className="font-serif italic text-sm border-b border-[#141414] pb-1 font-bold text-[#141414]">
              01_Fluent_Agent_Builder_Setup
            </h2>

            <div className="space-y-3 font-mono text-xs">
              <div>
                <label className="block font-bold text-[10px] uppercase tracking-wider mb-1 opacity-80">
                  LLM Provider Driver
                </label>
                <select
                  value={llmProvider}
                  onChange={(e) => setLlmProvider(e.target.value)}
                  className="w-full bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] p-2 font-mono text-xs focus:bg-white focus:outline-none"
                >
                  <option value="gemini">Google Gemini 3.6 Flash (.use_gemini())</option>
                  <option value="azure">Azure OpenAI GPT-4o (.use_azure_openai())</option>
                  <option value="openai">Standard OpenAI (.use_openai())</option>
                </select>
              </div>

              <div className="space-y-2 pt-2 border-t border-[#141414]/20">
                <label className="block font-bold text-[10px] uppercase tracking-wider opacity-80">
                  Core Infrastructure Modules
                </label>
                <label className="flex items-center space-x-2 text-[#141414] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={useMemoryCache}
                    onChange={(e) => setUseMemoryCache(e.target.checked)}
                    className="accent-[#141414]"
                  />
                  <span>TTL Memory Cache (.use_memory_cache())</span>
                </label>

                <label className="flex items-center space-x-2 text-[#141414] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={useEventBus}
                    onChange={(e) => setUseEventBus(e.target.checked)}
                    className="accent-[#141414]"
                  />
                  <span>Event Messaging Bus (.use_in_memory_bus())</span>
                </label>

                <label className="flex items-center space-x-2 text-[#141414] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={mcpEnabled}
                    onChange={(e) => setMcpEnabled(e.target.checked)}
                    className="accent-[#141414]"
                  />
                  <span>Discover MCP Servers (.discover_mcp_servers())</span>
                </label>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t-2 border-[#141414]">
            <div className="flex items-center justify-between mb-1.5 font-mono text-[10px] uppercase font-bold">
              <span>Generated_Builder_Python.py</span>
              <button
                onClick={handleCopyCode}
                className="text-[#141414] underline hover:no-underline flex items-center space-x-1"
              >
                {copied ? <Check className="w-3 h-3 text-emerald-700" /> : <Copy className="w-3 h-3" />}
                <span>{copied ? 'COPIED' : 'COPY'}</span>
              </button>
            </div>
            <pre className="bg-[#141414] text-[#E4E3E0] p-3 font-mono text-[10px] leading-relaxed overflow-x-auto border border-[#141414]">
              {generatedBuilderCode}
            </pre>
          </div>
        </div>

        {/* Right Column - Live Agent Execution Console */}
        <div className="lg:col-span-8 border-2 border-[#141414] bg-white/40 p-5 space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-[#141414] pb-2">
              <h2 className="font-serif italic text-sm font-bold text-[#141414] flex items-center space-x-2">
                <Bot className="w-4 h-4 text-[#141414]" />
                <span>02_Live_Agent_Execution_Terminal</span>
              </h2>
              {result && (
                <div className="flex items-center space-x-2 font-mono text-[10px]">
                  <span className="bg-[#141414] text-[#E4E3E0] px-2 py-0.5 font-bold uppercase">
                    EXEC_TIME: {result.execution_time_ms || 12} MS
                  </span>
                  <span className="border border-[#141414] px-2 py-0.5 font-bold uppercase text-[#141414]">
                    ID: {result.agent_id || 'AGENT_CORE'}
                  </span>
                </div>
              )}
            </div>

            {/* Input Row */}
            <div className="space-y-1.5">
              <label className="block font-mono text-[10px] font-bold uppercase tracking-wider text-[#141414]/80">
                PROMPT_QUERY_INPUT
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleRunAgent()}
                  placeholder="Ask the Enterprise Agent to perform a task..."
                  className="flex-1 bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] font-mono text-xs px-3 py-2 focus:bg-white focus:outline-none"
                />
                <button
                  onClick={handleRunAgent}
                  disabled={loading}
                  className="bg-[#141414] hover:bg-black text-[#E4E3E0] font-mono font-bold text-xs uppercase px-5 py-2 border border-[#141414] flex items-center space-x-2 transition-colors disabled:opacity-50"
                >
                  {loading ? (
                    <div className="w-4 h-4 border-2 border-[#E4E3E0] border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>EXECUTE_AGENT</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Results Output */}
            {result && (
              <div className="space-y-4 pt-2">
                <div className="bg-[#141414] text-[#E4E3E0] p-4 border-2 border-[#141414]">
                  <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-[#E4E3E0]/60 block mb-1">
                    SYNTHESIZED_RESPONSE_PAYLOAD
                  </span>
                  <p className="font-mono text-xs leading-relaxed">{result.response}</p>
                </div>

                {/* Execution Steps */}
                {result.steps && result.steps.length > 0 && (
                  <div className="space-y-2">
                    <span className="font-serif italic text-xs border-b border-[#141414] block pb-1 font-bold">
                      REASONING_AND_TOOL_STEPS
                    </span>
                    <div className="space-y-2">
                      {result.steps.map((step, idx) => (
                        <div key={idx} className="border border-[#141414] bg-white p-3 font-mono text-xs space-y-1">
                          <div className="flex items-center justify-between font-bold text-[#141414]">
                            <span className="flex items-center space-x-1">
                              <ChevronRight className="w-3.5 h-3.5" />
                              <span>STEP_{step.step_number}: {step.thought}</span>
                            </span>
                            {step.action_tool && (
                              <span className="bg-[#141414] text-[#E4E3E0] px-1.5 py-0.5 text-[10px]">
                                TOOL: {step.action_tool}
                              </span>
                            )}
                          </div>
                          {step.observation && (
                            <div className="bg-[#E4E3E0] p-2 text-[11px] border border-[#141414]/30">
                              OBSERVATION: {step.observation}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Telemetry Logs */}
                {result.trace_logs && result.trace_logs.length > 0 && (
                  <div>
                    <span className="font-mono text-[10px] font-bold uppercase tracking-widest opacity-60 block mb-1">
                      FRAMEWORK_TELEMETRY_LOGS
                    </span>
                    <div className="bg-[#141414] text-[#E4E3E0] p-2.5 font-mono text-[10px] space-y-1 overflow-x-auto">
                      {result.trace_logs.map((log, i) => (
                        <div key={i}>{log}</div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

