import React, { useState } from "react";
import { StockRow } from "../Common";
import { STOCKS } from "../../utils/constants";

/**
 * DiscoverPage - Stock discovery and screening
 * Features: Category tabs, stock list with trending charts, AI insights
 */
export function DiscoverPage() {
  const [activeTab, setActiveTab] = useState("top10");

  const tabs = [
    { id: "top10", label: "TOP 10", icon: "◆" },
    { id: "profitable", label: "HIGH PROFIT", icon: "▲" },
    { id: "upcoming", label: "UPCOMING", icon: "◉" },
    { id: "highRisk", label: "HIGH RISK", icon: "⚠" },
  ];

  const tagColors = {
    top10: "bg-green-900 text-green-400 border-green-700",
    profitable: "bg-emerald-900/60 text-emerald-400 border-emerald-700",
    upcoming: "bg-teal-900/60 text-teal-400 border-teal-700",
    highRisk: "bg-red-950/60 text-red-400 border-red-900",
  };

  return (
    <div className="space-y-5">
      {/* Header with search */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-green-300 font-mono font-bold text-xl">
            COMPANY DISCOVERY
          </h2>
          <p className="text-green-700 text-xs font-mono mt-0.5">
            AI-screened investment universe
          </p>
        </div>
        <div className="border border-green-800 rounded-lg px-3 py-2 flex items-center gap-2">
          <span className="text-green-600 text-xs font-mono">🔍</span>
          <input
            className="bg-transparent text-green-400 font-mono text-xs focus:outline-none w-32 placeholder-green-800"
            placeholder="SEARCH SYMBOL..."
          />
        </div>
      </div>

      {/* Category tabs */}
      <div className="flex gap-2 flex-wrap">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-lg border font-mono text-xs tracking-widest transition-colors ${
              activeTab === t.id
                ? tagColors[t.id]
                : "border-green-900 text-green-700 hover:border-green-700 hover:text-green-500"
            }`}
          >
            <span>{t.icon}</span> {t.label}
          </button>
        ))}
      </div>

      {/* Stock list */}
      <div className="border border-green-900 rounded-xl bg-black overflow-hidden">
        <div className="px-4 py-2 border-b border-green-900 flex items-center justify-between">
          <span className="text-green-500 font-mono text-xs tracking-widest">
            {tabs.find((t) => t.id === activeTab)?.label} STOCKS
          </span>
          <span className="text-green-700 text-xs font-mono">
            {STOCKS[activeTab].length} results
          </span>
        </div>
        <div className="px-4 py-2 grid grid-cols-4 md:grid-cols-6 gap-4 border-b border-green-950 text-green-700 text-xs font-mono tracking-widest">
          <span className="col-span-2">COMPANY</span>
          <span className="hidden md:block">TREND</span>
          <span>PRICE</span>
          <span>CHANGE</span>
          <span className="hidden md:block">MKT CAP</span>
        </div>
        {STOCKS[activeTab].map((s) => (
          <StockRow key={s.sym} stock={s} />
        ))}
      </div>

      {/* AI insights */}
      <div className="border border-green-900 rounded-xl bg-black p-4">
        <div className="text-green-500 font-mono text-xs tracking-widest mb-3">
          AGENT INSIGHTS
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {[
            {
              icon: "◆",
              title: "Momentum Signal",
              body: "NVDA, LLY showing strong upward momentum. Agent increased allocation by 12%.",
            },
            {
              icon: "▲",
              title: "Volume Anomaly",
              body: "IONQ trading 3.2x avg volume. Breakout pattern detected with 74% confidence.",
            },
            {
              icon: "⬡",
              title: "Risk Alert",
              body: "FFIE volatility at 180% 30-day avg. Agent has set strict loss limits at -5%.",
            },
          ].map((c) => (
            <div key={c.title} className="border border-green-900 rounded-lg p-3">
              <div className="text-green-500 font-mono text-sm mb-1">
                {c.icon} {c.title}
              </div>
              <p className="text-green-700 text-xs font-mono leading-relaxed">
                {c.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
