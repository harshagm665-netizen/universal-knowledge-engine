"use client";
import React, { useState } from 'react';
import SentinelFeed from '../components/SentinelFeed';

export default function Home() {
  const [logs, setLogs] = useState<string[]>(["[SYSTEM]: Nova Sentinel Online"]);

  const addLog = (msg: string) => {
    setLogs(prev => [`${new Date().toLocaleTimeString()} - ${msg}`, ...prev].slice(0, 10));
  };

  return (
    <main className="min-h-screen bg-[#050a0f] text-white p-6 font-mono selection:bg-[#00ff88] selection:text-black">
      <div className="flex justify-between items-center border-b border-[#00ff88]/20 pb-4 mb-8">
        <h1 className="text-2xl font-bold text-[#00ff88] tracking-tighter uppercase">
          SAVAGE SENTINEL v1.0 <span className="text-slate-500 text-sm">[PRESCHOOL TEACHER BOT]</span>
        </h1>
        <span className="text-slate-500 text-xs">SERVER_STATUS: ONLINE</span>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <SentinelFeed onAction={addLog} />
        </div>

        <div className="bg-[#0f172a] border border-slate-800 p-6 rounded-xl shadow-xl min-h-[400px]">
          <h3 className="text-slate-400 text-xs font-bold mb-4 uppercase tracking-[0.2em]">Live Action Logs</h3>
          <div className="space-y-3 text-sm">
            {logs.map((log, i) => (
              <div key={i} className={i === 0 ? "text-[#00ff88]" : "text-slate-500"}>
                {">"} {log}
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}