import React, { useState } from 'react';
import { Play, CheckCircle2, Clock, Terminal, ChevronRight, Code } from 'lucide-react';
import { ExampleMeta } from '../types';

export const ExampleRunner: React.FC = () => {
  const examples: ExampleMeta[] = [
    { id: '01', number: '01', title: '01 - Console Chat', description: 'Basic CLI Chat loop with @tool registration', path: 'examples/01-console-chat/main.py', category: 'Chat Engine' },
    { id: '02', number: '02', title: '02 - FastAPI Chat', description: 'FastAPI REST endpoint integration with Agent', path: 'examples/02-fastapi-chat/main.py', category: 'Web API' },
    { id: '03', number: '03', title: '03 - Streaming Chat', description: 'SSE Async Generator stream response', path: 'examples/03-streaming-chat/main.py', category: 'Streaming' },
    { id: '04', number: '04', title: '04 - Local Tools', description: 'Decorator & class-based tool registration', path: 'examples/04-local-tools/main.py', category: 'Tool Framework' },
    { id: '05', number: '05', title: '05 - MCP Tools', description: 'Single MCP server client & discovery', path: 'examples/05-mcp-tools/main.py', category: 'MCP' },
    { id: '06', number: '06', title: '06 - Multiple MCP', description: 'Multiple remote MCP servers discovery', path: 'examples/06-multiple-mcp/main.py', category: 'MCP' },
    { id: '07', number: '07', title: '07 - gRPC Service', description: 'Internal gRPC Service RPC communication', path: 'examples/07-grpc/main.py', category: 'gRPC' },
    { id: '08', number: '08', title: '08 - Memory Cache', description: 'In-memory TTL sliding cache integration', path: 'examples/08-memory-cache/main.py', category: 'Caching' },
    { id: '09', number: '09', title: '09 - Redis Cache', description: 'Distributed Redis caching driver', path: 'examples/09-redis-cache/main.py', category: 'Caching' },
    { id: '10', number: '10', title: '10 - Kafka Bus', description: 'Apache Kafka event bus publish/subscribe', path: 'examples/10-kafka/main.py', category: 'Messaging' },
    { id: '11', number: '11', title: '11 - RabbitMQ Bus', description: 'AMQP RabbitMQ event bus driver', path: 'examples/11-rabbitmq/main.py', category: 'Messaging' },
    { id: '12', number: '12', title: '12 - Plugin System', description: 'External plugin loader framework', path: 'examples/12-plugin/main.py', category: 'Plugins' },
    { id: '13', number: '13', title: '13 - Custom LLM', description: 'ILLMProvider custom driver implementation', path: 'examples/13-custom-llm/main.py', category: 'LLM' },
    { id: '14', number: '14', title: '14 - Custom Tool', description: 'Class-based ITool implementation', path: 'examples/14-custom-tool/main.py', category: 'Tool Framework' },
    { id: '15', number: '15', title: '15 - Production Blueprint', description: 'Full enterprise production template with DI', path: 'examples/15-production-template/main.py', category: 'Production' },
    { id: '16', number: '16', title: '16 - RAG & Doc Extractor', description: 'Document extraction tools & vector embeddings search', path: 'examples/16-rag-document-extractor/main.py', category: 'RAG & Vector' },
    { id: '17', number: '17', title: '17 - Enterprise Context Engine', description: 'Context Engine, Priority Token Budgeting & Providers', path: 'examples/17-context-engine/main.py', category: 'Context Engine' },
    { id: '18', number: '18', title: '18 - Enterprise Guardrails Engine', description: 'Guardrails Engine, Prompt Injection, PII, Tool Security', path: 'examples/18-guardrails-engine/main.py', category: 'Guardrails Engine' },
    { id: '19', number: '19', title: '19 - Governance & Resiliency', description: 'Model Routing Engine, Policy Engine, Feature Flags, Extension SDK & Resiliency', path: 'examples/19-enterprise-governance/main.py', category: 'Governance & Resiliency' },
  ];

  const [selectedEx, setSelectedEx] = useState<ExampleMeta>(examples[0]);
  const [running, setRunning] = useState(false);
  const [output, setOutput] = useState<string | null>(null);
  const [latency, setLatency] = useState<number | null>(null);

  const handleRunExample = async () => {
    setRunning(true);
    setOutput(null);
    setLatency(null);
    try {
      const res = await fetch('/api/python/run-script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scriptPath: selectedEx.path }),
      });
      const data = await res.json();
      setOutput(data.stdout || data.stderr || 'No output recorded.');
      setLatency(data.durationMs);
    } catch (err: any) {
      setOutput(`Error running script: ${err.message}`);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-2 border-[#141414] bg-white/40 p-5 space-y-4">
        <h2 className="font-serif italic text-sm font-bold border-b border-[#141414] pb-2 text-[#141414] flex items-center space-x-2">
          <Play className="w-4 h-4 text-[#141414]" />
          <span>Phase 21 - 15 Independently Runnable Enterprise Examples</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-2.5 mt-3">
          {examples.map((ex) => {
            const isSelected = selectedEx.id === ex.id;
            return (
              <button
                key={ex.id}
                onClick={() => {
                  setSelectedEx(ex);
                  setOutput(null);
                }}
                className={`p-2.5 border-2 border-[#141414] text-left font-mono text-xs transition-colors ${
                  isSelected
                    ? 'bg-[#141414] text-[#E4E3E0] font-bold'
                    : 'bg-white/50 text-[#141414] hover:bg-[#141414] hover:text-[#E4E3E0]'
                }`}
              >
                <div className="flex items-center justify-between font-bold mb-1 uppercase text-[11px]">
                  <span className="truncate">{ex.title}</span>
                </div>
                <p className="text-[10px] opacity-80 line-clamp-2 leading-snug">{ex.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Output Console for Selected Example */}
      <div className="border-2 border-[#141414] bg-white/40 p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-[#141414] pb-2">
          <div>
            <h3 className="font-mono text-xs font-bold uppercase text-[#141414] flex items-center space-x-2">
              <Code className="w-4 h-4 text-[#141414]" />
              <span>{selectedEx.title} // EXECUTION_TERMINAL</span>
            </h3>
            <p className="font-mono text-[10px] text-[#141414]/70 mt-0.5">{selectedEx.path}</p>
          </div>

          <button
            onClick={handleRunExample}
            disabled={running}
            className="bg-[#141414] hover:bg-black disabled:opacity-50 text-[#E4E3E0] font-mono font-bold text-xs uppercase px-4 py-2 border border-[#141414] flex items-center space-x-2 transition-colors"
          >
            {running ? (
              <div className="w-4 h-4 border-2 border-[#E4E3E0] border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>EXECUTE_EXAMPLE</span>
              </>
            )}
          </button>
        </div>

        {output ? (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-mono font-bold text-[#141414]">
              <span className="flex items-center space-x-1.5 uppercase">
                <Terminal className="w-3.5 h-3.5 text-[#141414]" />
                <span>SUBPROCESS_TERMINAL_STDOUT</span>
              </span>
              {latency && (
                <span className="bg-[#141414] text-[#E4E3E0] px-2 py-0.5 text-[10px]">
                  LATENCY: {latency} MS
                </span>
              )}
            </div>
            <pre className="bg-[#141414] text-[#E4E3E0] p-4 text-xs font-mono overflow-x-auto leading-relaxed border border-[#141414]">
              {output}
            </pre>
          </div>
        ) : (
          <div className="h-32 flex items-center justify-center border-2 border-dashed border-[#141414] font-mono text-xs text-[#141414]/70">
            [AWAITING_EXECUTION_TRIGGER] Click "EXECUTE_EXAMPLE" to execute Python script live.
          </div>
        )}
      </div>
    </div>
  );
};

