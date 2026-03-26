import React from "react";
import { fmt } from "../../utils/formatters";

/**
 * DashboardPage - Advanced analytics and performance metrics
 * Shows: P&L charts, monthly volume, performance ratios, sector distribution
 */
export function DashboardPage() {
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const pnlData = [1200, 3400, -800, 5600, 2100, 7800, -1200, 9400, 4300, 11200, 6700, 14800];
  const volData = [45, 67, 34, 89, 56, 103, 44, 127, 78, 142, 91, 168];
  const maxPnl = Math.max(...pnlData.map(Math.abs));
  const maxVol = Math.max(...volData);

  return (
    <div className="space-y-6">
      {/* KPI row */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["TOTAL PROFIT", "+$71,500", "green"],
          ["TOTAL LOSS", "-$2,000", "red"],
          ["NET P&L", "+$69,500", "green"],
          ["WIN RATE", "73.4%", "green"],
          ["AVG TRADE", "+$482", "green"],
          ["MAX DRAWDOWN", "-4.2%", "red"],
        ].map(([l, v, c]) => (
          <div
            key={l}
            className="border border-green-900 rounded-lg p-3 bg-black text-center"
          >
            <div className="text-green-700 text-xs font-mono mb-1 tracking-wider">
              {l}
            </div>
            <div
              className={`font-mono font-bold text-lg ${
                c === "green" ? "text-green-400" : "text-red-400"
              }`}
            >
              {v}
            </div>
          </div>
        ))}
      </div>

      {/* Monthly P&L Chart */}
      <div className="border border-green-900 rounded-xl bg-black p-5">
        <div className="text-green-500 font-mono text-xs tracking-widest mb-4">
          MONTHLY P&L (2024)
        </div>
        <div className="flex items-end gap-1.5 h-40">
          {pnlData.map((v, i) => {
            const h = (Math.abs(v) / maxPnl) * 100;
            const pos = v >= 0;
            return (
              <div key={i} className="flex-1 flex flex-col items-center gap-0.5">
                {pos ? (
                  <>
                    <div
                      style={{
                        height: `${h}%`,
                        backgroundColor: "#22c55e",
                        opacity: 0.8,
                      }}
                      className="w-full rounded-t transition-all hover:opacity-100"
                    />
                    <div className="h-px w-full bg-green-900" />
                  </>
                ) : (
                  <>
                    <div className="h-px w-full bg-green-900" />
                    <div
                      style={{
                        height: `${h}%`,
                        backgroundColor: "#ef4444",
                        opacity: 0.8,
                      }}
                      className="w-full rounded-b"
                    />
                  </>
                )}
              </div>
            );
          })}
        </div>
        <div className="flex gap-1.5 mt-2">
          {months.map((m) => (
            <div key={m} className="flex-1 text-center text-green-800 text-xs font-mono">
              {m.slice(0, 1)}
            </div>
          ))}
        </div>
      </div>

      {/* Volume + Performance Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Monthly trade volume */}
        <div className="border border-green-900 rounded-xl bg-black p-5">
          <div className="text-green-500 font-mono text-xs tracking-widest mb-4">
            MONTHLY TRADE VOLUME
          </div>
          <div className="flex items-end gap-1.5 h-28">
            {volData.map((v, i) => (
              <div
                key={i}
                style={{
                  height: `${(v / maxVol) * 100}%`,
                  background: `hsl(${140 + i * 2},60%,${30 + (v / maxVol) * 30}%)`,
                }}
                className="flex-1 rounded-t transition-all hover:opacity-100"
              />
            ))}
          </div>
          <div className="flex gap-1.5 mt-2">
            {months.map((m) => (
              <div key={m} className="flex-1 text-center text-green-800 text-xs font-mono">
                {m.slice(0, 1)}
              </div>
            ))}
          </div>
        </div>

        {/* Performance metrics */}
        <div className="border border-green-900 rounded-xl bg-black p-5">
          <div className="text-green-500 font-mono text-xs tracking-widest mb-4">
            AGENT PERFORMANCE METRICS
          </div>
          <div className="space-y-3">
            {[
              ["Calmar Ratio", "3.12", 90],
              ["Sortino Ratio", "4.87", 95],
              ["Max Favorable Excursion", "8.4%", 84],
              ["Profit Factor", "2.94", 85],
              ["Average Win / Loss", "3.2x", 80],
            ].map(([l, v, p]) => (
              <div key={l} className="flex items-center gap-3">
                <span className="text-green-700 text-xs font-mono w-44 shrink-0">
                  {l}
                </span>
                <div className="flex-1 h-1.5 bg-green-950 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-green-500 rounded-full"
                    style={{ width: `${p}%` }}
                  />
                </div>
                <span className="text-green-400 text-xs font-mono w-10 text-right">
                  {v}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Sector distribution */}
      <div className="border border-green-900 rounded-xl bg-black p-5">
        <div className="text-green-500 font-mono text-xs tracking-widest mb-4">
          TRADE DISTRIBUTION BY SECTOR
        </div>
        <div className="flex gap-4 flex-wrap">
          {[
            ["Technology", 42, "#22c55e"],
            ["Finance", 18, "#16a34a"],
            ["Healthcare", 14, "#15803d"],
            ["Energy", 10, "#166534"],
            ["Consumer", 8, "#14532d"],
            ["Other", 8, "#052e16"],
          ].map(([label, pct, color]) => (
            <div key={label} className="flex items-center gap-2 text-xs font-mono">
              <div
                className="w-3 h-3 rounded-sm"
                style={{ backgroundColor: color }}
              />
              <span className="text-green-600">{label}</span>
              <span className="text-green-400 font-bold">{pct}%</span>
            </div>
          ))}
        </div>
        <div className="flex h-6 rounded-lg overflow-hidden mt-3 gap-0.5">
          {[
            [42, "#22c55e"],
            [18, "#16a34a"],
            [14, "#15803d"],
            [10, "#166534"],
            [8, "#14532d"],
            [8, "#052e16"],
          ].map(([p, c], i) => (
            <div
              key={i}
              style={{ width: `${p}%`, backgroundColor: c }}
              className="h-full transition-all hover:opacity-80"
            />
          ))}
        </div>
      </div>
    </div>
  );
}
