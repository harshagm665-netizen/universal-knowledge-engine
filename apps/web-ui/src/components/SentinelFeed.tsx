"use client";
import React from 'react';

interface Props { onAction: (msg: string) => void; }

const SentinelFeed = ({ onAction }: Props) => {
  const triggerAction = async (endpoint: string, label: string) => {
    onAction(`Sending ${label} request...`);
    try {
      const res = await fetch(`http://localhost:8000/manual/${endpoint}`, { method: 'POST' });
      const data = await res.json();
      onAction(`${label} Result: ${data.status || "Success"}`);
    } catch (e) {
      onAction(`${label} Error: Backend unreachable at port 8000`);
    }
  };

  return (
    <div className="bg-[#0f172a] border border-[#00ff88]/30 rounded-lg overflow-hidden shadow-2xl">
      <div className="bg-[#00ff88] text-black px-4 py-2 text-xs font-bold flex justify-between uppercase">
        <span>LIVE_VISION_STREAM</span>
        <span className="animate-pulse">● REC</span>
      </div>
      
      {/* The Video Feed Container */}
      <div className="bg-black aspect-video flex items-center justify-center border-b border-[#00ff88]/10">
        <img 
          src="http://localhost:8000/video_feed" 
          alt="Sentinel Stream"
          className="w-full h-full object-contain"
          onError={(e) => {
            onAction("[ERROR]: Camera feed link broken.");
            e.currentTarget.src = "https://via.placeholder.com/640x480?text=FEED_OFFLINE";
          }}
        />
      </div>

      {/* Manual Override Buttons */}
      <div className="p-4 grid grid-cols-2 gap-4 bg-[#1e293b]">
        <button 
          onClick={() => triggerAction('analyze', 'Analysis')} 
          className="bg-blue-600 border-2 border-blue-400 text-white py-3 rounded font-bold hover:bg-blue-400 transition-all uppercase text-xs"
        >
          🔍 Analyze Frame
        </button>
        <button 
          onClick={() => triggerAction('wave', 'Social Wave')} 
          className="bg-green-600 border-2 border-green-400 text-white py-3 rounded font-bold hover:bg-green-400 transition-all uppercase text-xs"
        >
          👋 Force Wave
        </button>
      </div>
    </div>
  );
};

export default SentinelFeed;