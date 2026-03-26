import React, { useState, useEffect } from "react";
import { StatCard, MiniBar } from "../Common";
import { HOME_STATS, LIVE_TRADES } from "../../utils/constants";
import { fmt, fmtUSD, randInt, rand } from "../../utils/formatters";

/**
 * HomePage - Dashboard overview showing agent performance
 * Displays: AUM, profit, win rate, Sharpe ratio, live trades, diagnostics
 */
export function HomePage({ setPage }) {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setTick((x) => x + 1), 2000);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="space-y-6">
      {/* Hero section */}
      <div className="relative rounded-xl border border-green-800 bg-gradient-to-br from-green-950/60 to-black overflow-hidden p-6 md:p-8">
        <div
          className="absolute right-0 top-0 bottom-0 w-64 opacity-10 pointer-events-none"
          style={{
            backgroundImage:
              "repeating-linear-gradient(45deg,#0f2 0,#0f2 1px,transparent 0,transparent 50%)",
            backgroundSize: "8px 8px",
          }}
        />
        <div className="text-green-600 font-mono text-xs tracking-widest mb-2">
          ◈ AUTONOMOUS AGENT STATUS
        </div>
        <h1 className="text-3xl md:text-4xl font-mono font-black text-green-300 leading-tight">
          REINFORCEMENT
          <br />
          <span className="text-green-500">LEARNING TRADER</span>
        </h1>
        <p className="text-green-700 font-mono text-sm mt-3 max-w-md">
          Your AI agent uses deep Q-networks and policy gradient methods to
          autonomously execute optimal trades across 500+ instruments.
        </p>
        <div className="flex gap-3 mt-5 flex-wrap">
          <button
            onClick={() => setPage("portfolio")}
            className="bg-green-500 hover:bg-green-400 text-black font-mono font-bold px-5 py-2.5 rounded-lg text-sm transition-colors tracking-wider"
          >
            VIEW PORTFOLIO →
          </button>
          <button
            onClick={() => setPage("wallet")}
            className="border border-green-700 hover:border-green-500 text-green-400 font-mono px-5 py-2.5 rounded-lg text-sm transition-colors tracking-wider"
          >
            FUND AGENT
          </button>
        </div>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {HOME_STATS.map((s) => (
          <StatCard
            key={s.label}
            {...s}
            mini={<MiniBar data={Array.from({ length: 8 }, () => randInt(40, 100))} />}
          />
        ))}
      </div>

      {/* Live feed + diagnostics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Live trades feed */}
        <div className="border border-green-900 rounded-xl bg-black overflow-hidden">
          <div className="px-4 py-3 border-b border-green-900 flex items-center justify-between">
            <span className="text-green-500 font-mono text-xs tracking-widest">
              LIVE AGENT FEED
            </span>
            <span className="flex items-center gap-1.5 text-green-600 text-xs font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
              LIVE
            </span>
          </div>
          <div className="p-3 space-y-1 h-48 overflow-y-auto">
            {LIVE_TRADES.map((t) => (
              <div
                key={t.id}
                className="flex items-center gap-2 text-xs font-mono py-1 border-b border-green-950"
              >
                <span
                  className={`px-1.5 py-0.5 rounded text-xs font-bold ${
                    t.action === "BUY"
                      ? "bg-green-900 text-green-400"
                      : "bg-red-950 text-red-400"
                  }`}
                >
                  {t.action}
                </span>
                <span className="text-green-300">{t.sym}</span>
                <span className="text-green-700">×{t.qty}</span>
                <span className="text-green-600 flex-1">${fmt(t.price)}</span>
                <span className={t.pnl >= 0 ? "text-green-400" : "text-red-400"}>
                  {fmtUSD(t.pnl)}
                </span>
                <span className="text-green-800">{t.time}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Agent diagnostics */}
        <div className="border border-green-900 rounded-xl bg-black overflow-hidden">
          <div className="px-4 py-3 border-b border-green-900">
            <span className="text-green-500 font-mono text-xs tracking-widest">
              AGENT DIAGNOSTICS
            </span>
          </div>
          <div className="p-4 space-y-3">
            {[
              ["EPSILON (exploration)", "0.023", "87%"],
              ["Q-VALUE CONVERGENCE", "0.9981", "99%"],
              ["REWARD SIGNAL", "12.47", "94%"],
              ["POLICY ENTROPY", "0.134", "72%"],
              ["MEMORY BUFFER", "94K / 100K", "94%"],
            ].map(([label, val, pct]) => (
              <div key={label}>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-green-700">{label}</span>
                  <span className="text-green-400">{val}</span>
                </div>
                <div className="w-full h-1 bg-green-950 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-green-500 rounded-full transition-all"
                    style={{ width: pct }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
