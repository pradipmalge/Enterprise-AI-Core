import React, { useState } from 'react';
import { FileSearch, Database, Cpu, Play, Check, Copy, Sparkles, FileText, Layers, Search, Clock, ChevronRight } from 'lucide-react';

const SAMPLE_DOCS = [
  {
    title: "Enterprise SLA & Pricing 2026",
    text: `ENTERPRISE SERVICE LEVEL AGREEMENT (SLA) & FINANCIAL TERMS 2026

1. COMMENCEMENT & PARTIES
This Service Level Agreement is effective from March 1, 2026 through February 28, 2028.
Parties: Apex Cloud Infrastructure Inc ("Provider") and Global Enterprise Corp ("Client").

2. SERVICE AVAILABILITY & SLA METRICS
- System Uptime Commitment: Provider guarantees 99.99% monthly uptime for Core Cloud APIs.
- Penalty Credits: If uptime falls below 99.90%, Client receives 15% billing credit.
- Response Time SLA: Severity 1 incidents shall be acknowledged within 15 minutes.

3. FINANCIAL CONSIDERATIONS & PRICING
- Annual Base Contract Value: $1,250,000 USD billed quarterly in advance ($312,500 USD per quarter).
- Overage Rate: Excess compute hours billed at $0.045 per vCPU hour.
- Payment Terms: Net 30 days.

4. COMPLIANCE & SECURITY GOVERNANCE
- Data Sovereignty: All Client data hosted within EU-Central-1 and US-East-1 regions.
- Certifications: Provider maintains SOC2 Type II, ISO 27001, and HIPAA compliance.`
  },
  {
    title: "API Architecture & Security Policy",
    text: `ENTERPRISE SECURITY & API GOVERNANCE POLICY v4.2

1. AUTHENTICATION & TOKEN DURATION
All API endpoints require OAuth 2.0 with mTLS encryption. Access tokens expire after 3600 seconds (1 hour). Refresh tokens are valid for 14 days.

2. RATE LIMITING & THROTTLING
- Standard Tier: 1,000 requests/min per IP.
- Enterprise Platinum Tier: 50,000 requests/min with guaranteed burst capacity.
- Exceeding limit triggers HTTP 429 Too Many Requests with Retry-After header.

3. DATA RETENTION & BACKUPS
- Log Retention: Audit trail logs retained for 7 years in immutable WORM storage.
- Automated Backups: Database snapshots taken every 15 minutes with RPO of <5 mins and RTO of <15 mins.`
  }
];

export const RagStudio: React.FC = () => {
  const [selectedDocIndex, setSelectedDocIndex] = useState(0);
  const [customDocText, setCustomDocText] = useState(SAMPLE_DOCS[0].text);
  const [ingested, setIngested] = useState(false);
  const [ingestStatus, setIngestStatus] = useState<any>(null);
  const [extractedDetails, setExtractedDetails] = useState<any>(null);
  const [extracting, setExtracting] = useState(false);
  
  // Vector search
  const [searchQuery, setSearchQuery] = useState("uptime commitment and credits");
  const [searchResults, setSearchResults] = useState<any>(null);
  const [searching, setSearching] = useState(false);

  // RAG Prompt Chat
  const [ragPrompt, setRagPrompt] = useState("What are the quarterly billing amount, uptime SLA, and penalty credits?");
  const [ragResponse, setRagResponse] = useState<any>(null);
  const [prompting, setPrompting] = useState(false);

  const handleSelectSample = (idx: number) => {
    setSelectedDocIndex(idx);
    setCustomDocText(SAMPLE_DOCS[idx].text);
    setIngested(false);
    setIngestStatus(null);
    setExtractedDetails(null);
    setSearchResults(null);
    setRagResponse(null);
  };

  // 1. Ingest Document Python Script Execution
  const handleIngest = async () => {
    setIngested(false);
    setIngestStatus("Indexing document chunks into Vector Embeddings Index...");
    try {
      const pyCode = `
import json
from enterprise_ai_core.rag import ingest_document_to_rag

text = """${customDocText.replace(/"""/g, '\\"\\"\\"')}\"""
res = ingest_document_to_rag(text, source_name="Uploaded_Doc.txt")
print(res)
`;
      const res = await fetch('/api/python/run-script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: pyCode }),
      });
      const data = await res.json();
      const parsed = JSON.parse(data.stdout || '{}');
      setIngestStatus(parsed);
      setIngested(true);
    } catch (e: any) {
      setIngestStatus({ error: e.message });
    }
  };

  // 2. Extract Document Details Tool
  const handleExtractDetails = async () => {
    setExtracting(true);
    setExtractedDetails(null);
    try {
      const pyCode = `
import json
from enterprise_ai_core.rag import extract_document_details

text = """${customDocText.replace(/"""/g, '\\"\\"\\"')}\"""
res = extract_document_details(text)
print(res)
`;
      const res = await fetch('/api/python/run-script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: pyCode }),
      });
      const data = await res.json();
      const parsed = JSON.parse(data.stdout || '{}');
      setExtractedDetails(parsed);
    } catch (e: any) {
      setExtractedDetails({ error: e.message });
    } finally {
      setExtracting(false);
    }
  };

  // 3. Vector Similarity Search Tool
  const handleVectorSearch = async () => {
    setSearching(true);
    setSearchResults(null);
    try {
      const pyCode = `
import json
from enterprise_ai_core.rag import ingest_document_to_rag, search_knowledge_base

text = """${customDocText.replace(/"""/g, '\\"\\"\\"')}\"""
ingest_document_to_rag(text, source_name="Uploaded_Doc.txt")
res = search_knowledge_base("${searchQuery.replace(/"/g, '\\"')}")
print(res)
`;
      const res = await fetch('/api/python/run-script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: pyCode }),
      });
      const data = await res.json();
      const parsed = JSON.parse(data.stdout || '{}');
      setSearchResults(parsed);
    } catch (e: any) {
      setSearchResults({ error: e.message });
    } finally {
      setSearching(false);
    }
  };

  // 4. RAG Agent Prompt Query
  const handleRagPrompt = async () => {
    setPrompting(true);
    setRagResponse(null);
    try {
      const res = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `Using the document tools, answer this query: "${ragPrompt}". Document content preview: ${customDocText.slice(0, 300)}...`,
          provider: 'gemini',
          tools: ['extract_document_details', 'search_knowledge_base']
        }),
      });
      const data = await res.json();
      setRagResponse(data);
    } catch (e: any) {
      setRagResponse({ error: e.message });
    } finally {
      setPrompting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Overview Banner */}
      <div className="border-2 border-[#141414] bg-white/40 p-5 space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-[#141414] pb-3">
          <div>
            <h2 className="font-serif italic text-base font-bold text-[#141414] flex items-center space-x-2">
              <FileSearch className="w-5 h-5 text-[#141414]" />
              <span>Phase 24 - RAG Document Extractor & Vector Embeddings Studio</span>
            </h2>
            <p className="font-mono text-xs text-[#141414]/80 mt-0.5 uppercase">
              Extract key details, clauses, metrics & execute vector semantic search tools across unstructured documents.
            </p>
          </div>
          <span className="font-mono text-[10px] font-bold uppercase bg-[#141414] text-[#E4E3E0] px-3 py-1 self-start md:self-auto">
            STATUS: RAG_ENGINE_READY
          </span>
        </div>

        {/* Sample Selectors */}
        <div className="flex flex-wrap items-center gap-2 pt-1 font-mono text-xs">
          <span className="font-bold text-[10px] uppercase opacity-70">SELECT_PRESET_DOCUMENT:</span>
          {SAMPLE_DOCS.map((doc, idx) => (
            <button
              key={idx}
              onClick={() => handleSelectSample(idx)}
              className={`px-3 py-1 border border-[#141414] font-bold uppercase transition-colors ${
                selectedDocIndex === idx
                  ? 'bg-[#141414] text-[#E4E3E0]'
                  : 'bg-white/60 text-[#141414] hover:bg-[#141414] hover:text-[#E4E3E0]'
              }`}
            >
              {doc.title}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Document Editor & Ingestion Panel */}
        <div className="lg:col-span-6 border-2 border-[#141414] bg-white/40 p-5 space-y-4 flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center justify-between border-b border-[#141414] pb-2 font-mono text-xs font-bold text-[#141414]">
              <span className="flex items-center space-x-1.5 uppercase">
                <FileText className="w-4 h-4 text-[#141414]" />
                <span>01_Raw_Document_Source</span>
              </span>
              <span className="text-[10px] opacity-70">{customDocText.length} CHARACTERS</span>
            </div>

            <textarea
              value={customDocText}
              onChange={(e) => setCustomDocText(e.target.value)}
              rows={12}
              className="w-full bg-[#141414] text-[#E4E3E0] p-3 font-mono text-xs leading-relaxed border border-[#141414] focus:outline-none focus:ring-1 focus:ring-[#141414]"
              placeholder="Paste raw contract, SLA, technical spec, or financial report..."
            />
          </div>

          <div className="space-y-3 pt-2 border-t border-[#141414]">
            <div className="flex gap-2">
              <button
                onClick={handleIngest}
                className="flex-1 bg-[#141414] hover:bg-black text-[#E4E3E0] font-mono font-bold text-xs uppercase px-4 py-2 border border-[#141414] flex items-center justify-center space-x-2 transition-colors"
              >
                <Database className="w-3.5 h-3.5" />
                <span>INGEST_&_INDEX_CHUNK_EMBEDDINGS</span>
              </button>

              <button
                onClick={handleExtractDetails}
                disabled={extracting}
                className="bg-white hover:bg-[#141414] hover:text-[#E4E3E0] text-[#141414] font-mono font-bold text-xs uppercase px-4 py-2 border-2 border-[#141414] flex items-center space-x-2 transition-colors disabled:opacity-50"
              >
                {extracting ? (
                  <div className="w-3.5 h-3.5 border-2 border-[#141414] border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>EXTRACT_DETAILS_TOOL</span>
                  </>
                )}
              </button>
            </div>

            {/* Ingestion Output Status */}
            {ingestStatus && (
              <div className="bg-[#141414] text-[#E4E3E0] p-3 font-mono text-[10px] border border-[#141414]">
                <span className="font-bold text-emerald-400 block mb-1">VECTOR_INDEX_INGESTION_RESPONSE:</span>
                <pre className="whitespace-pre-wrap">{JSON.stringify(ingestStatus, null, 2)}</pre>
              </div>
            )}
          </div>
        </div>

        {/* Extracted Details & Vector Search Tools Output */}
        <div className="lg:col-span-6 border-2 border-[#141414] bg-white/40 p-5 space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="border-b border-[#141414] pb-2 font-mono text-xs font-bold text-[#141414] flex items-center justify-between">
              <span className="flex items-center space-x-1.5 uppercase">
                <Layers className="w-4 h-4 text-[#141414]" />
                <span>02_Extracted_Entities_&_Clauses</span>
              </span>
            </div>

            {extractedDetails ? (
              <div className="bg-[#141414] text-[#E4E3E0] p-4 font-mono text-xs space-y-3 border border-[#141414]">
                <div className="border-b border-[#E4E3E0]/20 pb-2">
                  <span className="text-[10px] text-[#E4E3E0]/60 block uppercase font-bold">DOCUMENT_SUMMARY</span>
                  <p className="font-bold text-emerald-400 mt-0.5">{extractedDetails.document_summary}</p>
                </div>

                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div className="border border-[#E4E3E0]/20 p-2">
                    <span className="text-[9px] text-[#E4E3E0]/60 uppercase block font-bold">EXTRACTED_DATES</span>
                    <ul className="list-disc list-inside mt-1 text-[#E4E3E0]">
                      {extractedDetails.extracted_dates?.map((d: string, i: number) => (
                        <li key={i}>{d}</li>
                      )) || <li>None</li>}
                    </ul>
                  </div>

                  <div className="border border-[#E4E3E0]/20 p-2">
                    <span className="text-[9px] text-[#E4E3E0]/60 uppercase block font-bold">FINANCIAL_FIGURES</span>
                    <ul className="list-disc list-inside mt-1 text-[#E4E3E0]">
                      {extractedDetails.financial_terms?.map((f: string, i: number) => (
                        <li key={i}>{f}</li>
                      )) || <li>None</li>}
                    </ul>
                  </div>
                </div>

                <div>
                  <span className="text-[10px] text-[#E4E3E0]/60 block uppercase font-bold">KEY_IDENTIFIED_SECTIONS</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {extractedDetails.key_sections?.map((s: string, i: number) => (
                      <span key={i} className="bg-[#E4E3E0] text-[#141414] font-bold px-1.5 py-0.5 text-[10px]">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-40 flex flex-col items-center justify-center border-2 border-dashed border-[#141414] font-mono text-xs text-[#141414]/70 p-4 text-center">
                <span>[EXTRACTOR_TOOL_IDLE]</span>
                <span className="text-[10px] opacity-80 mt-1">
                  Click "EXTRACT_DETAILS_TOOL" to execute entity regex & structural detail extraction.
                </span>
              </div>
            )}

            {/* Vector Similarity Search Tool UI */}
            <div className="space-y-2 pt-2 border-t border-[#141414]">
              <span className="font-mono text-xs font-bold uppercase text-[#141414] block">
                03_Vector_Semantic_Search_Tool
              </span>
              <div className="flex gap-2 font-mono text-xs">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Vector search prompt (e.g., uptime guarantee)..."
                  className="flex-1 bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] p-2 font-mono text-xs focus:bg-white focus:outline-none"
                />
                <button
                  onClick={handleVectorSearch}
                  disabled={searching}
                  className="bg-[#141414] hover:bg-black text-[#E4E3E0] px-4 py-2 font-bold uppercase border border-[#141414] flex items-center space-x-1"
                >
                  <Search className="w-3.5 h-3.5" />
                  <span>SEARCH</span>
                </button>
              </div>

              {searchResults && (
                <div className="bg-[#141414] text-[#E4E3E0] p-3 font-mono text-[10px] space-y-2 border border-[#141414] max-h-48 overflow-y-auto">
                  <div className="flex justify-between border-b border-[#E4E3E0]/20 pb-1 font-bold">
                    <span>QUERY: "{searchResults.query}"</span>
                    <span>MATCHES: {searchResults.total_matches || 0}</span>
                  </div>
                  {searchResults.matches?.map((m: any, idx: number) => (
                    <div key={idx} className="border border-[#E4E3E0]/20 p-2 space-y-1">
                      <div className="flex justify-between text-emerald-400 font-bold">
                        <span>CHUNK #{m.chunk_index}</span>
                        <span>SIMILARITY: {m.similarity_score}</span>
                      </div>
                      <p className="text-[#E4E3E0]/90 leading-tight">{m.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* RAG Agent Prompt Question Answering Console */}
      <div className="border-2 border-[#141414] bg-white/40 p-5 space-y-4">
        <div className="border-b border-[#141414] pb-2 font-mono text-xs font-bold text-[#141414] flex items-center justify-between">
          <span className="flex items-center space-x-2 uppercase">
            <Cpu className="w-4 h-4 text-[#141414]" />
            <span>04_RAG_Agent_Prompt_Console_(AI_Tool_Calling)</span>
          </span>
          <span className="text-[10px] opacity-70">TOOLS: [extract_document_details, search_knowledge_base]</span>
        </div>

        <div className="flex flex-col sm:flex-row gap-2">
          <input
            type="text"
            value={ragPrompt}
            onChange={(e) => setRagPrompt(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleRagPrompt()}
            placeholder="Ask AI to extract or answer details using document tools..."
            className="flex-1 bg-[#E4E3E0] border-2 border-[#141414] text-[#141414] p-2.5 font-mono text-xs focus:bg-white focus:outline-none"
          />
          <button
            onClick={handleRagPrompt}
            disabled={prompting}
            className="bg-[#141414] hover:bg-black text-[#E4E3E0] font-mono font-bold text-xs uppercase px-5 py-2.5 border border-[#141414] flex items-center justify-center space-x-2 transition-colors disabled:opacity-50"
          >
            {prompting ? (
              <div className="w-4 h-4 border-2 border-[#E4E3E0] border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>EXECUTE_RAG_PROMPT</span>
              </>
            )}
          </button>
        </div>

        {ragResponse && (
          <div className="space-y-3 pt-2">
            <div className="bg-[#141414] text-[#E4E3E0] p-4 border-2 border-[#141414]">
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-[#E4E3E0]/60 block mb-1">
                SYNTHESIZED_RAG_RESPONSE
              </span>
              <p className="font-mono text-xs leading-relaxed">{ragResponse.response}</p>
            </div>

            {ragResponse.steps && (
              <div className="space-y-2">
                <span className="font-serif italic text-xs font-bold border-b border-[#141414] block pb-1">
                  RAG_TOOL_CALLING_EXECUTIVE_STEPS
                </span>
                {ragResponse.steps.map((s: any, idx: number) => (
                  <div key={idx} className="border border-[#141414] bg-white p-3 font-mono text-xs space-y-1">
                    <div className="flex justify-between font-bold text-[#141414]">
                      <span className="flex items-center space-x-1">
                        <ChevronRight className="w-3.5 h-3.5" />
                        <span>STEP_{s.step_number}: {s.thought}</span>
                      </span>
                      {s.action_tool && (
                        <span className="bg-[#141414] text-[#E4E3E0] px-1.5 py-0.5 text-[10px]">
                          TOOL: {s.action_tool}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
