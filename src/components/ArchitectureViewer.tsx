import React, { useState } from 'react';
import { Cpu, Layers, GitFork, MessageSquare, Repeat, Wrench, Globe, Shield, Copy, Check } from 'lucide-react';

export const ArchitectureViewer: React.FC = () => {
  const [activeDiagram, setActiveDiagram] = useState('overall');
  const [copied, setCopied] = useState(false);

  const diagramSpecs: Record<string, { title: string; desc: string; mermaid: string }> = {
    overall: {
      title: "01_OVERALL_CLEAN_ARCHITECTURE_SPECIFICATION",
      desc: "Strict separation of concerns into Domain Abstractions, Core Framework Engine, Infrastructure Drivers, and Presentation Interfaces.",
      mermaid: `graph TD
    subgraph Presentation ["Presentation Layer"]
        FastAPI["FastAPI / Web API"]
        Console["Console Application"]
        gRPCServer["gRPC RPC Server"]
    end

    subgraph CoreEngine ["Enterprise Core Engine"]
        Agent["EnterpriseAgent"]
        Builder["AgentBuilder"]
        Planner["ExecutionPlanner"]
        Registry["ToolRegistry"]
        DI["ServiceCollection / IoC Container"]
    end

    subgraph Domain ["Domain Abstractions (SOLID Interfaces)"]
        ILLM["ILLMProvider"]
        ITool["ITool"]
        IMCP["IMCPClient"]
        ICache["ICache"]
        IMemory["IMemoryProvider"]
        IBus["IMessageBus"]
    end

    subgraph Infra ["Infrastructure Layer"]
        Gemini["Google Gemini Driver"]
        Azure["Azure OpenAI Driver"]
        Redis["Redis Distributed Cache"]
        Kafka["Kafka Event Bus"]
        MCPImpl["MCP Client Pool"]
    end

    Presentation --> Agent
    Agent --> Builder
    Agent --> Planner
    Agent --> Registry
    CoreEngine --> Domain
    Infra --> Domain`
    },
    agent_loop: {
      title: "02_AGENT_EXECUTION_LOOP_SEQUENCE",
      desc: "Detailed step-by-step reasoning, tool execution, observation feedback, and cache update loop.",
      mermaid: `sequenceDiagram
    autonumber
    actor User
    participant Agent as EnterpriseAgent
    participant Cache as Memory/Redis Cache
    participant Planner as ExecutionPlanner
    participant Tool as ToolRegistry / MCP
    participant Bus as EventPublisher

    User->>Agent: chat("Find customer 101 and summarize orders")
    Agent->>Cache: get("agent:query:...")
    alt Cache Hit
        Cache-->>Agent: Return Cached Answer
    else Cache Miss
        Agent->>Planner: create_plan(query)
        Planner-->>Agent: AgentSteps [Step 1: Tool Call, Step 2: Synthesis]
        loop For each step
            Agent->>Tool: execute_tool("customer_search")
            Tool-->>Agent: Observation Data
        end
        Agent->>Bus: publish("agent.completed")
        Agent->>Cache: set("agent:query:...", answer)
    end
    Agent-->>User: Result<ResponseContext>`
    },
    mcp: {
      title: "03_MCP_MODEL_CONTEXT_PROTOCOL_INTEGRATION",
      desc: "Remote tool discovery, session connection pooling, and healthcheck retry policies.",
      mermaid: `graph LR
    Agent["EnterpriseAgent"] --> Pool["MCP Connection Pool"]
    Pool --> Client1["MCP Client (Database Server)"]
    Pool --> Client2["MCP Client (Knowledge Base)"]
    Pool --> Client3["MCP Client (CRM Server)"]

    Client1 -->|JSON-RPC| Remote1["Remote MCP Server #1"]
    Client2 -->|JSON-RPC| Remote2["Remote MCP Server #2"]
    Client3 -->|JSON-RPC| Remote3["Remote MCP Server #3"]`
    },
    messaging: {
      title: "04_EVENT_DRIVEN_MESSAGING_BUS_PIPELINE",
      desc: "Asynchronous publish-subscribe messaging across In-Memory, Kafka, and RabbitMQ.",
      mermaid: `graph TD
    Publisher["EventPublisher"] -->|publish_event| Bus["IMessageBus Interface"]
    Bus -->|In-Memory| MemBus["InMemoryBus Handler"]
    Bus -->|Apache Kafka| KafkaBus["KafkaBus Producer"]
    Bus -->|RabbitMQ| RabbitBus["RabbitMQ AMQP Exchange"]

    MemBus --> Sub1["Audit Logging Plugin"]
    KafkaBus --> Sub2["Analytics Microservice"]
    RabbitBus --> Sub3["Notification Gateway"]`
    }
  };

  const current = diagramSpecs[activeDiagram] || diagramSpecs.overall;

  const handleCopyMermaid = () => {
    navigator.clipboard.writeText(current.mermaid);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Selector Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-2 border-[#141414] bg-white/40 p-4">
        <div>
          <h2 className="font-serif italic text-base font-bold text-[#141414] flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-[#141414]" />
            <span>Phase 20 - System Architecture Diagrams</span>
          </h2>
          <p className="font-mono text-xs text-[#141414]/70 mt-0.5 uppercase">
            Clean Architecture, Component Specifications, and Execution Flows.
          </p>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {[
            { id: 'overall', label: '01_Clean_Architecture', icon: Layers },
            { id: 'agent_loop', label: '02_Execution_Loop', icon: Repeat },
            { id: 'mcp', label: '03_MCP_Protocol', icon: Globe },
            { id: 'messaging', label: '04_Event_Bus', icon: GitFork },
          ].map((item) => {
            const Icon = item.icon;
            const isActive = activeDiagram === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveDiagram(item.id)}
                className={`px-3 py-1.5 font-mono text-xs uppercase tracking-wider border border-[#141414] flex items-center space-x-1.5 transition-colors ${
                  isActive
                    ? 'bg-[#141414] text-[#E4E3E0] font-bold'
                    : 'bg-white/50 text-[#141414] hover:bg-[#141414] hover:text-[#E4E3E0]'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Main Diagram Mermaid Code Block */}
        <div className="lg:col-span-8 border-2 border-[#141414] bg-white/40 p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#141414] pb-2">
            <div>
              <h3 className="font-mono text-xs font-bold uppercase text-[#141414]">{current.title}</h3>
              <p className="font-serif italic text-xs text-[#141414]/80 mt-0.5">{current.desc}</p>
            </div>
            <button
              onClick={handleCopyMermaid}
              className="font-mono text-[10px] font-bold uppercase bg-[#141414] text-[#E4E3E0] hover:bg-black px-2.5 py-1 border border-[#141414] flex items-center space-x-1 shrink-0"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              <span>{copied ? 'COPIED' : 'COPY MERMAID'}</span>
            </button>
          </div>

          <div className="bg-[#141414] text-[#E4E3E0] p-4 font-mono text-xs border border-[#141414] overflow-x-auto leading-relaxed">
            <pre className="whitespace-pre-wrap">{current.mermaid}</pre>
          </div>
        </div>

        {/* Guarantees Box */}
        <div className="lg:col-span-4 border-2 border-[#141414] bg-white/40 p-5 space-y-4">
          <h3 className="font-serif italic text-sm font-bold border-b border-[#141414] pb-2 text-[#141414]">
            05_Architectural_Guarantees
          </h3>
          <ul className="space-y-3 font-mono text-xs text-[#141414]">
            <li className="border border-[#141414] bg-white p-3 space-y-1">
              <div className="flex items-center space-x-1.5 font-bold uppercase text-[#141414]">
                <Shield className="w-4 h-4 text-[#141414]" />
                <span>SOLID Principles</span>
              </div>
              <p className="text-[11px] opacity-80 leading-snug">
                Infrastructure drivers implement domain interfaces directly without leaking framework dependencies.
              </p>
            </li>

            <li className="border border-[#141414] bg-white p-3 space-y-1">
              <div className="flex items-center space-x-1.5 font-bold uppercase text-[#141414]">
                <Layers className="w-4 h-4 text-[#141414]" />
                <span>IoC DI Container</span>
              </div>
              <p className="text-[11px] opacity-80 leading-snug">
                Native `ServiceCollection` & `ServiceProvider` support singleton, scoped, and transient resolution.
              </p>
            </li>

            <li className="border border-[#141414] bg-white p-3 space-y-1">
              <div className="flex items-center space-x-1.5 font-bold uppercase text-[#141414]">
                <Wrench className="w-4 h-4 text-[#141414]" />
                <span>Production Resiliency</span>
              </div>
              <p className="text-[11px] opacity-80 leading-snug">
                Built-in retry backoff policies, circuit breakers, dead-letter queues, and telemetry event streaming.
              </p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

