import React, { useState, useEffect } from "react";
import { StatCard, Sparkline } from "../Common";
import { PORTFOLIO_HOLDINGS, LIVE_TRADES } from "../../utils/constants";
import { fmt, fmtUSD, fmtPct, rand } from "../../utils/formatters";

/**
 * PortfolioPage - Live portfolio management
 * Shows: Holdings, P&L, live prices, trade history
 * Real-time price updates with sparkline trends
 */
export function PortfolioPage() {
  const [prices, setPrices] = useState(
    PORTFOLIO_HOLDINGS.reduce((a, h) => ({ ...a, [h.sym]: h.currPrice }), {})
  );

  // Simulate real-time price updates
  useEffect(() => {
    const t = setInterval(() => {
      setPrices((prev) =>
        Object.fromEntries(
          Object.entries(prev).map(([k, v]) => [
            k,
            +(v + rand(-1.5, 1.5)).toFixed(2),
          ])
        )
      );
    }, 1500);
    return () => clearInterval(t);
  }, []);

  const totalVal = PORTFOLIO_HOLDINGS.reduce(
    (s, h) => s + h.qty * prices[h.sym],
    0
  );
  const totalPnL = PORTFOLIO_HOLDINGS.reduce((s, h) => s + h.pnl, 0);

  return (
    <div className="space-y-6">
      {/* Portfolio summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="PORTFOLIO VALUE"
          value={fmtUSD(totalVal)}
          sub={fmtUSD(totalPnL) + " unrealized"}
          positive={totalPnL > 0}
          icon="◆"
        />
        <StatCard
          label="TOTAL P&L"
          value={fmtUSD(totalPnL)}
          sub="+12.4% overall"
          positive={true}
          icon="▲"
        />
        <StatCard
          label="OPEN POSITIONS"
          value="6"
          sub="Across 3 sectors"
          positive={true}
          icon="◈"
        />
        <StatCard
          label="DAILY TRADES"
          value="127"
          sub="Avg $1,847 / trade"
          positive={true}
          icon="≋"
        />
      </div>

      {/* Holdings table */}
      <div className="border border-green-900 rounded-xl bg-black overflow-hidden">
        <div className="px-4 py-3 border-b border-green-900 flex items-center justify-between">
          <span className="text-green-500 font-mono text-xs tracking-widest">
            AUTONOMOUS HOLDINGS
          </span>
          <span className="flex items-center gap-1.5 text-green-600 text-xs font-mono">
            <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
            REAL-TIME
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-green-950">
                {[
                  "SYMBOL",
                  "QTY",
                  "AVG COST",
                  "CURR PRICE",
                  "MKT VALUE",
                  "P&L",
                  "RETURN",
                  "TREND",
                ].map((h) => (
                  <th
                    key={h}
                    className="px-4 py-2 text-left text-green-700 text-xs font-mono tracking-widest"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {PORTFOLIO_HOLDINGS.map((h) => {
                const curr = prices[h.sym];
                const val = h.qty * curr;
                const pnl = h.qty * (curr - h.avgCost);
                const ret = ((curr - h.avgCost) / h.avgCost) * 100;
                const pos = pnl >= 0;

                return (
                  <tr
                    key={h.sym}
                    className="border-b border-green-950/50 hover:bg-green-950/20 transition-colors"
                  >
                    <td className="px-4 py-3 font-mono text-sm font-bold text-green-300">
                      {h.sym}
                    </td>
                    <td className="px-4 py-3 font-mono text-sm text-green-500">
                      {h.qty}
                    </td>
                    <td className="px-4 py-3 font-mono text-sm text-green-600">
                      ${fmt(h.avgCost)}
                    </td>
                    <td className="px-4 py-3 font-mono text-sm text-green-300">
                      ${fmt(curr)}
                    </td>
                    <td className="px-4 py-3 font-mono text-sm text-green-400">
                      ${fmt(val)}
                    </td>
                    <td
                      className={`px-4 py-3 font-mono text-sm font-bold ${
                        pos ? "text-green-400" : "text-red-400"
                      }`}
                    >
                      {fmtUSD(pnl)}
                    </td>
                    <td
                      className={`px-4 py-3 font-mono text-sm ${
                        pos ? "text-green-400" : "text-red-400"
                      }`}
                    >
                      {fmtPct(ret)}
                    </td>
                    <td className="px-4 py-3">
                      <Sparkline positive={pos} width={60} height={24} />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Trade history log */}
      <div className="border border-green-900 rounded-xl bg-black overflow-hidden">
        <div className="px-4 py-3 border-b border-green-900">
          <span className="text-green-500 font-mono text-xs tracking-widest">
            AGENT TRADE LOG
          </span>
        </div>
        <div className="divide-y divide-green-950">
          {LIVE_TRADES.map((t) => (
            <div
              key={t.id}
              className="flex items-center gap-3 px-4 py-3 hover:bg-green-950/20"
            >
              <span
                className={`px-2 py-1 rounded text-xs font-mono font-bold ${
                  t.action === "BUY"
                    ? "bg-green-900/60 text-green-400 border border-green-700"
                    : "bg-red-950/60 text-red-400 border border-red-900"
                }`}
              >
                {t.action}
              </span>
              <span className="text-green-300 font-mono text-sm w-14 font-bold">
                {t.sym}
              </span>
              <span className="text-green-700 font-mono text-xs">
                {t.qty} shares @ ${fmt(t.price)}
              </span>
              <span className="flex-1 text-green-800 font-mono text-xs hidden md:block">
                {t.time}
              </span>
              <span
                className={`font-mono text-sm font-bold ${
                  t.pnl >= 0 ? "text-green-400" : "text-red-400"
                }`}
              >
                {fmtUSD(t.pnl)}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-mono border ${
                  t.status === "FILLED"
                    ? "text-green-500 border-green-800"
                    : "text-yellow-500 border-yellow-900"
                }`}
              >
                {t.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
