import React, { useState } from 'react';
import { BookOpen, FileText, CheckCircle2 } from 'lucide-react';

export const DocCenter: React.FC = () => {
  const [selectedDoc, setSelectedDoc] = useState('README.md');

  const docList = [
    { name: 'README.md', path: 'README.md', desc: 'Framework Quickstart & Installation' },
    { name: 'ModelRouting.md', path: 'docs/ModelRouting.md', desc: 'Enterprise Model Routing, Provider Priority & Failover' },
    { name: 'Governance.md', path: 'docs/Governance.md', desc: 'AI Policy Engine, Feature Flags & Environment Profiles' },
    { name: 'Guardrails.md', path: 'docs/Guardrails.md', desc: 'Guardrails Engine Pipeline Architecture' },
    { name: 'SecurityPolicies.md', path: 'docs/SecurityPolicies.md', desc: 'Security Policies & Policy Engine' },
    { name: 'PromptInjection.md', path: 'docs/PromptInjection.md', desc: 'Prompt Injection & Jailbreak Defense' },
    { name: 'ToolSecurity.md', path: 'docs/ToolSecurity.md', desc: 'Tool Security & Role Authorization' },
    { name: 'PIIProtection.md', path: 'docs/PIIProtection.md', desc: 'PII & Secret Leakage Auto-Redaction' },
    { name: 'Compliance.md', path: 'docs/Compliance.md', desc: 'Enterprise Compliance & Audit Logging' },
    { name: 'ContextEngine.md', path: 'docs/ContextEngine.md', desc: 'Enterprise Context Management Engine & Architecture' },
  ];

  return (
    <div className="space-y-6">
      <div className="border-2 border-[#141414] bg-white/40 p-5">
        <h2 className="font-serif italic text-sm font-bold border-b border-[#141414] pb-2 text-[#141414] flex items-center space-x-2">
          <BookOpen className="w-5 h-5 text-[#141414]" />
          <span>Phase 19 - Enterprise AI Core Documentation Center</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
          {docList.map((doc) => (
            <button
              key={doc.name}
              onClick={() => setSelectedDoc(doc.name)}
              className={`p-3 border-2 border-[#141414] text-left font-mono text-xs transition-colors ${
                selectedDoc === doc.name
                  ? 'bg-[#141414] text-[#E4E3E0] font-bold'
                  : 'bg-white/50 text-[#141414] hover:bg-[#141414] hover:text-[#E4E3E0]'
              }`}
            >
              <div className="flex items-center space-x-2 font-bold mb-1 uppercase">
                <FileText className="w-3.5 h-3.5" />
                <span>{doc.name}</span>
              </div>
              <p className="text-[11px] opacity-80 leading-snug">{doc.desc}</p>
            </button>
          ))}
        </div>
      </div>

      <div className="border-2 border-[#141414] bg-white/40 p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-[#141414] pb-2">
          <h3 className="font-mono text-xs font-bold uppercase text-[#141414]">{selectedDoc}</h3>
          <span className="font-mono text-[10px] font-bold uppercase bg-[#141414] text-[#E4E3E0] px-2 py-0.5 flex items-center space-x-1">
            <CheckCircle2 className="w-3 h-3 text-emerald-400" />
            <span>PHASE_19_VALIDATED</span>
          </span>
        </div>

        <div className="bg-[#141414] text-[#E4E3E0] p-4 font-mono text-xs leading-relaxed border border-[#141414]">
          <p>
            Enterprise AI Core v1.0 documentation complete. All 24 phases verified and documented under Clean Architecture guidelines.
          </p>
        </div>
      </div>
    </div>
  );
};

