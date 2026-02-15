import React, { useState, useEffect } from 'react';

const SentinelFeed = () => {
  const [isLive, setIsLive] = useState(false);

  return (
    <div className="flex flex-col items-center bg-slate-900 p-6 rounded-xl border border-cyan-500 shadow-[0_0_15px_rgba(0,255,255,0.3)]">
      <h2 className="text-cyan-400 font-mono text-xl mb-4 tracking-widest">
        LIVE_SENTINEL_FEED // BLUEPRINT_MODE
      </h2>
      
      <div className="relative border-2 border-cyan-800 rounded-lg overflow-hidden bg-black aspect-video w-full max-w-2xl">
        {/* This draws the stream directly from your FastAPI backend */}
        <img 
          src="http://localhost:8000/video_feed" 
          alt="Sentinel Stream"
          className={`w-full h-full object-cover ${!isLive ? 'opacity-50 grayscale' : ''}`}
          onLoad={() => setIsLive(true)}
          onError={() => setIsLive(false)}
        />
        
        {!isLive && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-red-500 font-mono animate-pulse">SYSTEM_OFFLINE</span>
          </div>
        )}
      </div>

      <div className="mt-4 flex gap-4">
        <button 
          onClick={async () => await fetch('http://localhost:8000/manual/wave', { method: 'POST' })}
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-md transition-all active:scale-95"
        >
          TRIGGER_WAVE
        </button>
      </div>
    </div>
  );
};

export default SentinelFeed;