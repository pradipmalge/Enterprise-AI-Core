import React, { useState } from 'react';
import { CheckCircle2, Play, ShieldCheck, Clock, Terminal } from 'lucide-react';
import { TestResult } from '../types';

export const TestRunner: React.FC = () => {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<TestResult | null>(null);

  const handleRunTests = async () => {
    setRunning(true);
    try {
      const res = await fetch('/api/python/run-tests', { method: 'POST' });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-2 border-[#141414] bg-white/40 p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-[#141414] pb-3">
          <div>
            <h2 className="font-serif italic text-sm font-bold text-[#141414] flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-[#141414]" />
              <span>Phase 22 - Unit & Integration Test Suite</span>
            </h2>
            <p className="font-mono text-xs text-[#141414]/70 mt-0.5 uppercase">
              Validate Clean Architecture, DI container, Agent execution, and Tool Registry assertions.
            </p>
          </div>

          <button
            onClick={handleRunTests}
            disabled={running}
            className="bg-[#141414] hover:bg-black disabled:opacity-50 text-[#E4E3E0] font-mono font-bold text-xs uppercase px-4 py-2 border border-[#141414] flex items-center space-x-2 transition-colors"
          >
            {running ? (
              <div className="w-4 h-4 border-2 border-[#E4E3E0] border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>EXECUTE_TEST_SUITE</span>
              </>
            )}
          </button>
        </div>

        {result ? (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono">
              <div className="bg-[#141414] text-[#E4E3E0] p-4 border border-[#141414]">
                <span className="text-[10px] font-bold uppercase tracking-widest text-[#E4E3E0]/60">
                  SUITE_TEST_STATUS
                </span>
                <p className="text-sm font-bold text-emerald-400 mt-1 flex items-center space-x-1.5 uppercase">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>{result.success ? 'ALL_TESTS_PASSED' : 'TESTS_FAILED'}</span>
                </p>
              </div>

              <div className="bg-[#141414] text-[#E4E3E0] p-4 border border-[#141414]">
                <span className="text-[10px] font-bold uppercase tracking-widest text-[#E4E3E0]/60">
                  TOTAL_LATENCY
                </span>
                <p className="text-sm font-bold mt-1 flex items-center space-x-1.5 uppercase">
                  <Clock className="w-4 h-4 text-[#E4E3E0]" />
                  <span>{result.durationMs} MS</span>
                </p>
              </div>

              <div className="bg-[#141414] text-[#E4E3E0] p-4 border border-[#141414]">
                <span className="text-[10px] font-bold uppercase tracking-widest text-[#E4E3E0]/60">
                  COVERAGE_ASSERTION
                </span>
                <p className="text-sm font-bold mt-1 uppercase text-[#E4E3E0]">
                  TARGET &gt; 90% PASS
                </p>
              </div>
            </div>

            <div className="space-y-1.5">
              <span className="font-mono text-xs font-bold text-[#141414] uppercase flex items-center space-x-1.5">
                <Terminal className="w-3.5 h-3.5" />
                <span>UNITTEST_STDOUT_STREAM</span>
              </span>
              <pre className="bg-[#141414] text-[#E4E3E0] p-4 text-xs font-mono border border-[#141414] overflow-x-auto leading-relaxed">
                {result.stdout || result.stderr || 'Tests completed with zero errors.'}
              </pre>
            </div>
          </div>
        ) : (
          <div className="h-32 flex items-center justify-center border-2 border-dashed border-[#141414] font-mono text-xs text-[#141414]/70">
            [AWAITING_TEST_TRIGGER] Click "EXECUTE_TEST_SUITE" to execute unittest assertions.
          </div>
        )}
      </div>
    </div>
  );
};

