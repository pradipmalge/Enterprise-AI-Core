import React, { useState } from 'react';
import { Sparkles, Copy, Check, Download, Layers, ShieldCheck } from 'lucide-react';

export const CodeGenerator: React.FC = () => {
  const [provider, setProvider] = useState('azure');
  const [cacheType, setCacheType] = useState('memory');
  const [busType, setBusType] = useState('in_memory');
  const [includeMcp, setIncludeMcp] = useState(true);
  const [toolName, setToolName] = useState('customer_search');
  const [copied, setCopied] = useState(false);

  const generatedScript = `import asyncio
from enterprise_ai_core import EnterpriseAgent, tool

@tool(name="${toolName}", description="Search enterprise records")
def ${toolName}(query: str) -> str:
    return f"Record for '{query}': Active Enterprise Account"

async def main():
    agent = (
        EnterpriseAgent.builder()
            .${provider === 'gemini' ? 'use_gemini()' : provider === 'azure' ? 'use_azure_openai()' : 'use_openai()'}
            .${cacheType === 'redis' ? 'use_redis_cache()' : 'use_memory_cache()'}
            .${busType === 'kafka' ? 'use_kafka_bus()' : busType === 'rabbitmq' ? 'use_rabbitmq_bus()' : 'use_in_memory_bus()'}
            .register_tool(${toolName})
            ${includeMcp ? '.discover_mcp_servers()' : ''}
            .with_system_prompt("You are a clean-architecture enterprise agent.")
            .build()
    )

    response = await agent.chat("Find customer 101 and summarize their last three orders.")
    print("Agent Response:", response.value["response"])

if __name__ == "__main__":
    asyncio.run(main())
`;

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedScript);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-4 border-2 border-[#141414] bg-white/40 p-5 space-y-4">
          <div className="flex items-center space-x-2 border-b border-[#141414] pb-2">
            <Sparkles className="w-4 h-4 text-[#141414]" />
            <h2 className="font-serif italic text-sm font-bold text-[#141414]">Visual Agent Code Builder</h2>
          </div>

          <div className="space-y-3 font-mono text-xs">
            <div>
              <label className="block font-bold text-[10px] uppercase tracking-wider mb-1 text-[#141414]/80">
                LLM Provider Driver
              </label>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] p-2 font-mono text-xs focus:bg-white focus:outline-none"
              >
                <option value="azure">Azure OpenAI (.use_azure_openai())</option>
                <option value="gemini">Google Gemini (.use_gemini())</option>
                <option value="openai">OpenAI (.use_openai())</option>
              </select>
            </div>

            <div>
              <label className="block font-bold text-[10px] uppercase tracking-wider mb-1 text-[#141414]/80">
                Cache Layer
              </label>
              <select
                value={cacheType}
                onChange={(e) => setCacheType(e.target.value)}
                className="w-full bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] p-2 font-mono text-xs focus:bg-white focus:outline-none"
              >
                <option value="memory">In-Memory TTL Cache</option>
                <option value="redis">Distributed Redis Cache</option>
              </select>
            </div>

            <div>
              <label className="block font-bold text-[10px] uppercase tracking-wider mb-1 text-[#141414]/80">
                Messaging Bus
              </label>
              <select
                value={busType}
                onChange={(e) => setBusType(e.target.value)}
                className="w-full bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] p-2 font-mono text-xs focus:bg-white focus:outline-none"
              >
                <option value="in_memory">In-Memory Event Bus</option>
                <option value="kafka">Apache Kafka Bus</option>
                <option value="rabbitmq">RabbitMQ AMQP Bus</option>
              </select>
            </div>

            <div>
              <label className="block font-bold text-[10px] uppercase tracking-wider mb-1 text-[#141414]/80">
                Primary Tool Identifier
              </label>
              <input
                type="text"
                value={toolName}
                onChange={(e) => setToolName(e.target.value)}
                className="w-full bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] p-2 font-mono text-xs focus:bg-white focus:outline-none"
              />
            </div>

            <label className="flex items-center space-x-2 text-[#141414] pt-1 cursor-pointer">
              <input
                type="checkbox"
                checked={includeMcp}
                onChange={(e) => setIncludeMcp(e.target.checked)}
                className="accent-[#141414]"
              />
              <span>Discover Remote MCP Servers</span>
            </label>
          </div>
        </div>

        <div className="lg:col-span-8 border-2 border-[#141414] bg-white/40 p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-[#141414] pb-2">
            <h3 className="font-mono text-xs font-bold uppercase text-[#141414]">
              STANDALONE_PYTHON_SCRIPT_GENERATION.py
            </h3>
            <button
              onClick={handleCopy}
              className="bg-[#141414] hover:bg-black text-[#E4E3E0] font-mono font-bold text-xs uppercase px-3 py-1.5 border border-[#141414] flex items-center space-x-1.5"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'COPIED' : 'COPY SCRIPT'}</span>
            </button>
          </div>

          <pre className="bg-[#141414] text-[#E4E3E0] p-4 text-xs font-mono overflow-x-auto leading-relaxed border border-[#141414]">
            {generatedScript}
          </pre>
        </div>
      </div>
    </div>
  );
};

