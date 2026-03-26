import React from "react";
import { rand, randInt } from "../../utils/formatters";

/**
 * Sparkline - Animated miniature line chart
 * Used in stock rows and stat cards
 */
export function Sparkline({ positive = true, width = 80, height = 30 }) {
  const points = Array.from({ length: 20 }, (_, i) => {
    const base = positive ? 10 + i * 0.8 : 20 - i * 0.8;
    return base + rand(-3, 3);
  });
  const min = Math.min(...points);
  const max = Math.max(...points);
  const norm = (v) => height - ((v - min) / (max - min)) * height;
  const path = points.map((v, i) => `${(i / 19) * width},${norm(v)}`).join(" L ");
  
  return (
    <svg 
      width={width} 
      height={height} 
      viewBox={`0 0 ${width} ${height}`} 
      className="overflow-visible"
    >
      <polyline 
        points={path} 
        fill="none" 
        stroke={positive ? "#22c55e" : "#ef4444"} 
        strokeWidth="1.5" 
      />
    </svg>
  );
}

/**
 * MiniBar - Vertical bar chart component
 * Displays data as proportional bars
 */
export function MiniBar({ data, color = "#22c55e" }) {
  const max = Math.max(...data);
  return (
    <div className="flex items-end gap-0.5 h-8">
      {data.map((v, i) => (
        <div
          key={i}
          style={{ 
            height: `${(v / max) * 100}%`, 
            backgroundColor: color, 
            opacity: 0.7 + (i / data.length) * 0.3 
          }}
          className="flex-1 rounded-sm"
        />
      ))}
    </div>
  );
}

/**
 * GlitchText - Styled text with monospace font
 * Used for technical/cyberpunk aesthetic
 */
export function GlitchText({ text, className = "" }) {
  return (
    <span 
      className={`relative inline-block ${className}`} 
      style={{ fontFamily: "'Courier New', monospace" }}
    >
      {text}
    </span>
  );
}

/**
 * TerminalLine - Typing animation effect
 * Simulates terminal output with cursor
 */
export function TerminalLine({ text, delay = 0 }) {
  const [displayed, setDisplayed] = React.useState("");
  
  React.useEffect(() => {
    const timer = setTimeout(() => {
      let i = 0;
      const interval = setInterval(() => {
        setDisplayed(text.slice(0, i + 1));
        i++;
        if (i >= text.length) clearInterval(interval);
      }, 40);
      return () => clearInterval(interval);
    }, delay);
    return () => clearTimeout(timer);
  }, [text, delay]);
  
  return (
    <div className="text-green-400 text-xs font-mono">
      <span className="text-green-600">{">"}</span> {displayed}
      <span className="animate-pulse">█</span>
    </div>
  );
}

/**
 * StatCard - Reusable statistics display component
 * Shows metric, value, optional sub-text, and mini-chart
 */
export function StatCard({ label, value, sub, positive, icon, mini }) {
  return (
    <div className="relative border border-green-900 bg-black rounded-lg p-4 overflow-hidden group hover:border-green-500 transition-colors">
      <div className="absolute inset-0 bg-gradient-to-br from-green-950/30 to-transparent pointer-events-none" />
      <div className="relative">
        <div className="flex items-center justify-between mb-2">
          <span className="text-green-600 text-xs font-mono uppercase tracking-widest">{label}</span>
          {icon && <span className="text-green-500 text-lg">{icon}</span>}
        </div>
        <div className="text-2xl font-bold text-green-300 font-mono">{value}</div>
        {sub && (
          <div className={`text-xs mt-1 font-mono ${positive ? "text-green-400" : "text-red-400"}`}>
            {sub}
          </div>
        )}
        {mini && <div className="mt-2">{mini}</div>}
      </div>
    </div>
  );
}

/**
 * StockRow - Row component for displaying individual stock info
 * Includes price, change, trend chart, and sector tag
 */
export function StockRow({ stock, onSelect }) {
  const pos = stock.change >= 0;
  
  return (
    <div
      onClick={() => onSelect && onSelect(stock)}
      className="flex items-center justify-between px-4 py-3 border-b border-green-950 hover:bg-green-950/30 cursor-pointer transition-colors group"
    >
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded border border-green-700 flex items-center justify-center bg-green-950 text-green-400 text-xs font-mono font-bold">
          {stock.sym.slice(0, 2)}
        </div>
        <div>
          <div className="text-green-200 font-mono text-sm font-bold">{stock.sym}</div>
          <div className="text-green-700 text-xs truncate max-w-[120px]">{stock.name}</div>
        </div>
      </div>
      <div className="flex items-center gap-6">
        <Sparkline positive={pos} width={60} height={24} />
        <div className="text-right">
          <div className="text-green-300 font-mono text-sm">${Number(stock.price).toFixed(2)}</div>
          <div className={`text-xs font-mono ${pos ? "text-green-400" : "text-red-400"}`}>
            {stock.change >= 0 ? "+" : ""}{stock.change.toFixed(2)}%
          </div>
        </div>
        <div className="text-green-700 text-xs font-mono hidden md:block">{stock.mktCap}</div>
        <div className="px-2 py-0.5 rounded text-xs font-mono bg-green-950 text-green-500 border border-green-800 hidden lg:block">
          {stock.sector}
        </div>
      </div>
    </div>
  );
}

/**
 * ScanlineOverlay - Adds retro CRT scanline effect
 * Purely decorative for cyberpunk aesthetic
 */
export function ScanlineOverlay() {
  return (
    <div
      className="pointer-events-none fixed inset-0 z-[9999] opacity-[0.03]"
      style={{
        backgroundImage: "repeating-linear-gradient(0deg, #000 0px, #000 1px, transparent 1px, transparent 2px)",
      }}
    />
  );
}
