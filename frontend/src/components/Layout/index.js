import React, { useState, useEffect } from "react";
import { NAV_ITEMS } from "../../utils/constants";

/**
 * Sidebar - Main navigation component
 * Fixed left sidebar with navigation items and agent status
 * Responsive: collapses to icon-only on mobile
 */
export function Sidebar({ page, setPage }) {
  return (
    <aside className="fixed left-0 top-0 h-full w-16 md:w-56 border-r border-green-900 bg-black flex flex-col z-50">
      {/* Brand header */}
      <div className="p-4 border-b border-green-900">
        <div className="text-green-400 font-mono font-bold text-sm md:text-base tracking-widest">
          <span className="hidden md:inline">◈ APEX</span>
          <span className="text-green-600 hidden md:inline">_RL</span>
          <span className="md:hidden">◈</span>
        </div>
        <div className="text-green-700 text-xs font-mono hidden md:block mt-0.5">
          AGENT v4.2.1
        </div>
      </div>

      {/* Navigation menu */}
      <nav className="flex-1 py-4">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            onClick={() => setPage(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 text-left transition-all font-mono text-xs tracking-widest ${
              page === item.id
                ? "bg-green-950 text-green-300 border-r-2 border-green-400"
                : "text-green-700 hover:text-green-400 hover:bg-green-950/40"
            }`}
          >
            <span className="text-base">{item.icon}</span>
            <span className="hidden md:inline">{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Status footer */}
      <div className="p-4 border-t border-green-900 hidden md:block">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="text-green-600 text-xs font-mono">AGENT ACTIVE</span>
        </div>
        <div className="text-green-800 text-xs font-mono mt-1">TRADES: 1,247 today</div>
      </div>
    </aside>
  );
}

/**
 * Topbar - Header component with market data and user info
 * Shows live market indices, current time, and user profile
 */
export function Topbar({ user }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  return (
    <header className="fixed top-0 left-16 md:left-56 right-0 h-12 border-b border-green-900 bg-black/95 backdrop-blur flex items-center justify-between px-4 z-40">
      <div className="flex items-center gap-4">
        <div className="text-green-600 text-xs font-mono hidden sm:flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse inline-block" />
          MARKET OPEN
        </div>
        <div className="text-green-700 text-xs font-mono hidden md:block">
          SPX: <span className="text-green-400">5,234.18</span> <span className="text-green-600">+0.42%</span>
        </div>
        <div className="text-green-700 text-xs font-mono hidden lg:block">
          NDX: <span className="text-green-400">18,432.7</span> <span className="text-green-600">+0.61%</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="text-green-600 text-xs font-mono">{time.toLocaleTimeString()}</div>
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-full border border-green-700 bg-green-950 flex items-center justify-center text-green-400 text-xs font-mono font-bold">
            {user.charAt(0).toUpperCase()}
          </div>
          <span className="text-green-500 text-xs font-mono hidden sm:inline">{user}</span>
        </div>
      </div>
    </header>
  );
}
