"use client";
import React, { useState } from 'react';

export default function SavageDashboard() {
  const [status, setStatus] = useState("READY");

  const triggerWave = async () => {
    setStatus("WAVING...");
    await fetch('http://localhost:8000/manual/wave', { method: 'POST' });
    setTimeout(() => setStatus("READY"), 2000);
  };

  return (
    <div className="min-h-screen bg-black text-cyan-400 p-10 font-mono">
      <h1 className="text-3xl border-b border-cyan-900 pb-4 mb-8">NOVA_SENTINEL_V1.0</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        <div className="border border-cyan-800 p-4 bg-slate-900 rounded-lg">
          <h2 className="mb-4">LIVE_VISUAL_DATA</h2>
          <img src="http://localhost:8000/video_feed" className="w-full rounded border border-cyan-500" />
        </div>
        <div className="flex flex-col justify-center items-center gap-6">
          <div className="text-6xl font-bold tracking-tighter">{status}</div>
          <button onClick={triggerWave} className="px-8 py-4 border-2 border-cyan-400 hover:bg-cyan-400 hover:text-black transition-all">
            MANUAL_OVERRIDE_WAVE
          </button>
        </div>
      </div>
    </div>
  );
}