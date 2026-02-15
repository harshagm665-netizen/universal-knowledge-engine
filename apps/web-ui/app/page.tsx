"use client";
import React, { useState } from 'react';

export default function SavageDashboard() {
  const [log, setLog] = useState("System Ready...");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAction = async (endpoint: string) => {
    if (endpoint === 'analyze') setIsAnalyzing(true);
    try {
      const res = await fetch(`http://localhost:8000/manual/${endpoint}`, { method: 'POST' });
      const data = await res.json();
      setLog(`${endpoint.toUpperCase()}: ${JSON.stringify(data.detections || data.status)}`);
    } catch (err) {
      setLog("Connection Error: Is server running?");
    }
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen bg-black text-green-500 p-8 font-mono">
      <h1 className="text-3xl font-bold mb-6 border-b border-green-900 pb-2">
        SAVAGE SENTINEL v1.0 [PRESCHOOL TEACHER BOT]
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Camera Feed Section */}
        <div className="border-2 border-green-500 rounded-lg overflow-hidden bg-gray-900">
          <div className="p-2 bg-green-500 text-black font-bold flex justify-between">
            <span>LIVE VISION FEED</span>
            <span className="animate-pulse">● REC</span>
          </div>
          <img 
            src="http://localhost:8000/video_feed" 
            alt="Camera Feed" 
            className="w-full h-auto grayscale sepia hover:grayscale-0 transition-all"
          />
        </div>

        {/* Control Section */}
        <div className="flex flex-col gap-6">
          <div className="bg-gray-900 p-6 border border-green-800 rounded-lg shadow-lg">
            <h2 className="text-xl mb-4 text-white">Manual Override</h2>
            <div className="flex gap-4">
              <button 
                onClick={() => handleAction('analyze')}
                disabled={isAnalyzing}
                className="flex-1 bg-blue-900 hover:bg-blue-700 border border-blue-400 p-4 rounded font-bold transition-all disabled:opacity-50"
              >
                {isAnalyzing ? "THINKING..." : "🔍 ANALYZE FRAME"}
              </button>
              <button 
                onClick={() => handleAction('wave')}
                className="flex-1 bg-green-900 hover:bg-green-700 border border-green-400 p-4 rounded font-bold transition-all"
              >
                👋 FORCE WAVE
              </button>
            </div>
          </div>

          <div className="bg-gray-900 p-6 border border-green-800 rounded-lg h-48 overflow-y-auto">
            <h2 className="text-sm text-gray-500 mb-2 uppercase tracking-widest">Action Logs</h2>
            <p className="text-green-400">{">"} {log}</p>
          </div>
        </div>
      </div>
    </div>
  );
}