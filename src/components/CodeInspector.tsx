import React, { useState, useEffect } from 'react';
import { FileCode2, Folder, FileText, Search, Copy, Check, ChevronRight, ChevronDown } from 'lucide-react';
import { FileNode } from '../types';

export const CodeInspector: React.FC = () => {
  const [tree, setTree] = useState<FileNode[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>("enterprise_ai_core/__init__.py");
  const [fileContent, setFileContent] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [copied, setCopied] = useState(false);
  const [expandedDirs, setExpandedDirs] = useState<Record<string, boolean>>({
    enterprise_ai_core: true,
    examples: true,
    docs: false,
    tests: false,
  });

  useEffect(() => {
    fetchTree();
    readFile("enterprise_ai_core/__init__.py");
  }, []);

  const fetchTree = async () => {
    try {
      const res = await fetch("/api/files/tree");
      const data = await res.json();
      setTree(data.tree || []);
    } catch (e) {
      console.error(e);
    }
  };

  const readFile = async (path: string) => {
    setLoading(true);
    setSelectedFile(path);
    try {
      const res = await fetch(`/api/files/read?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      setFileContent(data.content || "");
    } catch (e) {
      console.error(e);
      setFileContent("# Error reading file");
    } finally {
      setLoading(false);
    }
  };

  const toggleDir = (dirPath: string) => {
    setExpandedDirs((prev) => ({ ...prev, [dirPath]: !prev[dirPath] }));
  };

  const handleCopyContent = () => {
    navigator.clipboard.writeText(fileContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderNode = (node: FileNode) => {
    if (search && !node.name.toLowerCase().includes(search.toLowerCase()) && !node.isDirectory) {
      return null;
    }

    if (node.isDirectory) {
      const isExpanded = expandedDirs[node.path] ?? false;
      return (
        <div key={node.path} className="space-y-0.5">
          <button
            onClick={() => toggleDir(node.path)}
            className="w-full flex items-center space-x-1.5 px-2 py-1 text-xs text-[#141414] hover:bg-[#141414] hover:text-[#E4E3E0] font-mono text-left font-bold transition-colors"
          >
            {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
            <Folder className="w-3.5 h-3.5" />
            <span className="truncate">{node.name}</span>
          </button>
          {isExpanded && node.children && (
            <div className="pl-3 border-l-2 border-[#141414] space-y-0.5 ml-2">
              {node.children.map((child) => renderNode(child))}
            </div>
          )}
        </div>
      );
    }

    const isSelected = selectedFile === node.path;
    return (
      <button
        key={node.path}
        onClick={() => readFile(node.path)}
        className={`w-full flex items-center space-x-1.5 px-2 py-1 text-xs font-mono text-left transition-colors ${
          isSelected
            ? 'bg-[#141414] text-[#E4E3E0] font-bold'
            : 'text-[#141414] hover:bg-[#141414]/10'
        }`}
      >
        <FileCode2 className="w-3.5 h-3.5 shrink-0" />
        <span className="truncate">{node.name}</span>
      </button>
    );
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Sidebar File Tree */}
        <div className="lg:col-span-4 border-2 border-[#141414] bg-white/40 p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-[#141414] pb-2">
            <h3 className="font-serif italic text-xs font-bold text-[#141414] flex items-center space-x-1.5">
              <Folder className="w-4 h-4 text-[#141414]" />
              <span>Workspace Source Tree</span>
            </h3>
            <span className="text-[10px] text-[#141414]/70 font-mono font-bold">PYTHON_PKG</span>
          </div>

          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-[#141414]" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="SEARCH_FILES..."
              className="w-full bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] pl-8 pr-2 py-1.5 text-xs font-mono focus:outline-none focus:bg-white"
            />
          </div>

          <div className="space-y-1 max-h-[600px] overflow-y-auto pr-1">
            {tree.map((node) => renderNode(node))}
          </div>
        </div>

        {/* Code Content Viewer */}
        <div className="lg:col-span-8 border-2 border-[#141414] bg-white/40 p-5 flex flex-col space-y-3">
          <div className="flex items-center justify-between border-b border-[#141414] pb-2">
            <div className="flex items-center space-x-2">
              <FileText className="w-4 h-4 text-[#141414]" />
              <span className="text-xs font-mono font-bold text-[#141414]">{selectedFile}</span>
            </div>
            <button
              onClick={handleCopyContent}
              className="font-mono text-[10px] font-bold uppercase bg-[#141414] text-[#E4E3E0] hover:bg-black px-2.5 py-1 border border-[#141414] flex items-center space-x-1"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'COPIED' : 'COPY FILE'}</span>
            </button>
          </div>

          {loading ? (
            <div className="h-96 flex items-center justify-center font-mono text-xs text-[#141414]">
              LOADING_SOURCE_STREAM...
            </div>
          ) : (
            <pre className="bg-[#141414] text-[#E4E3E0] p-4 text-xs font-mono overflow-x-auto leading-relaxed border border-[#141414] max-h-[650px]">
              {fileContent}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
};

