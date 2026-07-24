import React, { useState } from 'react';
import { Header } from './components/Header';
import { AgentPlayground } from './components/AgentPlayground';
import { RagStudio } from './components/RagStudio';
import { ArchitectureViewer } from './components/ArchitectureViewer';
import { CodeInspector } from './components/CodeInspector';
import { DocCenter } from './components/DocCenter';
import { ExampleRunner } from './components/ExampleRunner';
import { TestRunner } from './components/TestRunner';
import { CodeGenerator } from './components/CodeGenerator';

export default function App() {
  const [activeTab, setActiveTab] = useState('playground');

  return (
    <div className="min-h-screen bg-[#E4E3E0] text-[#141414] font-sans flex flex-col p-2 sm:p-4 md:p-6 border-[6px] sm:border-[10px] md:border-[12px] border-[#141414] selection:bg-[#141414] selection:text-[#E4E3E0]">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 my-4">
        {activeTab === 'playground' && <AgentPlayground />}
        {activeTab === 'rag' && <RagStudio />}
        {activeTab === 'architecture' && <ArchitectureViewer />}
        {activeTab === 'inspector' && <CodeInspector />}
        {activeTab === 'docs' && <DocCenter />}
        {activeTab === 'examples' && <ExampleRunner />}
        {activeTab === 'tests' && <TestRunner />}
        {activeTab === 'generator' && <CodeGenerator />}
      </main>

      <footer className="mt-6 pt-4 border-t-2 border-[#141414] flex flex-col sm:flex-row justify-between items-center text-[10px] font-mono uppercase tracking-tight gap-2">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 bg-[#141414] rounded-full" />
            <span className="font-bold tracking-widest">SYSTEM_STATUS // HEALTHY</span>
          </div>
          <div className="hidden md:flex items-center gap-2">
            <div className="w-2.5 h-2.5 border border-[#141414] rounded-full" />
            <span className="font-bold tracking-widest">CLEAN_ARCH_v1.0.0</span>
          </div>
        </div>
        <div className="opacity-70 text-right">
          ENTERPRISE_AI_CORE // SPECIFICATION_VIEW_v1.0_PROD
        </div>
      </footer>
    </div>
  );
}

