import React from 'react';
import { Bot, Cpu, FileCode2, BookOpen, Terminal, CheckCircle2, Play, Sparkles, FileSearch } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'playground', label: 'Agent_Playground', icon: Bot },
    { id: 'rag', label: 'RAG_&_Doc_Extractor', icon: FileSearch },
    { id: 'architecture', label: 'System_Architecture', icon: Cpu },
    { id: 'inspector', label: 'Code_Inspector', icon: FileCode2 },
    { id: 'docs', label: 'Documentation', icon: BookOpen },
    { id: 'examples', label: '19_Runnable_Examples', icon: Play },
    { id: 'tests', label: 'Test_Suite', icon: CheckCircle2 },
    { id: 'generator', label: 'Code_Generator', icon: Sparkles },
  ];

  return (
    <header className="border-b-2 border-[#141414] pb-4 mb-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-baseline gap-4 mb-5">
        <div className="flex flex-col">
          <span className="text-[10px] font-bold tracking-widest uppercase opacity-60">
            Project Framework // Python 3.10
          </span>
          <h1 className="text-3xl md:text-5xl font-black tracking-tighter uppercase leading-none text-[#141414]">
            Enterprise-AI-Core
          </h1>
        </div>

        <div className="flex flex-col md:items-end">
          <span className="font-mono text-xs md:text-sm font-bold bg-[#141414] text-[#E4E3E0] px-2.5 py-1 uppercase tracking-tight">
            VERSION 1.0_PROD_READY
          </span>
          <div className="text-[11px] font-serif italic mt-1.5 opacity-90 text-[#141414]">
            Clean Architecture / SOLID / Enterprise Grade
          </div>
        </div>
      </div>

      {/* Grid Tab Navigation */}
      <nav className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-1.5 pt-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center justify-center space-x-1.5 px-2 py-2 text-xs font-mono uppercase tracking-wider border border-[#141414] transition-colors ${
                isActive
                  ? 'bg-[#141414] text-[#E4E3E0] font-bold'
                  : 'bg-white/40 text-[#141414] hover:bg-[#141414] hover:text-[#E4E3E0]'
              }`}
            >
              <Icon className="w-3.5 h-3.5 shrink-0" />
              <span className="truncate">{tab.label}</span>
            </button>
          );
        })}
      </nav>
    </header>
  );
};

