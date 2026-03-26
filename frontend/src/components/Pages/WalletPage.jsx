import React, { useState } from "react";
import { TRANSACTION_HISTORY } from "../../utils/constants";
import { fmtUSD } from "../../utils/formatters";

/**
 * WalletPage - Wallet management and transactions
 * Features: Balance display, deposit/withdraw, payment methods, transaction history
 */
export function WalletPage() {
  const [amount, setAmount] = useState("");
  const [method, setMethod] = useState("card");
  const [tab, setTab] = useState("deposit");

  const quickAmounts = [500, 1000, 5000, 10000, 25000, 50000];

  return (
    <div className="space-y-6">
      {/* Balance cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Main balance */}
        <div className="border border-green-700 rounded-xl bg-gradient-to-br from-green-950/60 to-black p-5 col-span-1 md:col-span-2">
          <div className="text-green-600 font-mono text-xs tracking-widest mb-1">
            TOTAL WALLET BALANCE
          </div>
          <div className="text-4xl font-mono font-black text-green-300 mt-2">
            $48,247.63
          </div>
          <div className="flex gap-4 mt-4">
            <div>
              <div className="text-green-700 text-xs font-mono">AVAILABLE</div>
              <div className="text-green-400 font-mono font-bold">$12,500.00</div>
            </div>
            <div className="w-px bg-green-900" />
            <div>
              <div className="text-green-700 text-xs font-mono">IN POSITIONS</div>
              <div className="text-green-400 font-mono font-bold">$35,747.63</div>
            </div>
            <div className="w-px bg-green-900" />
            <div>
              <div className="text-green-700 text-xs font-mono">PENDING</div>
              <div className="text-yellow-500 font-mono font-bold">$0.00</div>
            </div>
          </div>
        </div>

        {/* Agent allocation */}
        <div className="border border-green-900 rounded-xl bg-black p-5">
          <div className="text-green-600 font-mono text-xs tracking-widest mb-3">
            AGENT ALLOCATION
          </div>
          <div className="space-y-2">
            {[
              ["Conservative", "20%", "#166534"],
              ["Balanced", "50%", "#16a34a"],
              ["Aggressive", "30%", "#22c55e"],
            ].map(([l, p, c]) => (
              <div key={l}>
                <div className="flex justify-between text-xs font-mono mb-0.5">
                  <span className="text-green-700">{l}</span>
                  <span className="text-green-400">{p}</span>
                </div>
                <div className="h-1.5 bg-green-950 rounded-full overflow-hidden">
                  <div
                    style={{ width: p, backgroundColor: c }}
                    className="h-full rounded-full"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Deposit/Withdraw section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Deposit/Withdraw form */}
        <div className="border border-green-900 rounded-xl bg-black overflow-hidden">
          <div className="flex border-b border-green-900">
            {["deposit", "withdraw"].map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`flex-1 py-3 text-xs font-mono uppercase tracking-widest transition-colors ${
                  tab === t
                    ? "bg-green-950 text-green-300 border-b-2 border-green-500"
                    : "text-green-700 hover:text-green-500"
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          <div className="p-5 space-y-4">
            {/* Quick select amounts */}
            <div>
              <div className="text-green-600 text-xs font-mono mb-2 tracking-widest">
                QUICK SELECT (USD)
              </div>
              <div className="grid grid-cols-3 gap-2">
                {quickAmounts.map((a) => (
                  <button
                    key={a}
                    onClick={() => setAmount(String(a))}
                    className={`border rounded-lg py-2 text-xs font-mono transition-colors ${
                      amount === String(a)
                        ? "border-green-500 bg-green-950 text-green-300"
                        : "border-green-900 text-green-600 hover:border-green-700"
                    }`}
                  >
                    ${a.toLocaleString()}
                  </button>
                ))}
              </div>
            </div>

            {/* Custom amount */}
            <div>
              <label className="block text-green-600 text-xs font-mono mb-1 tracking-widest">
                CUSTOM AMOUNT
              </label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-green-600 font-mono text-sm">
                  $
                </span>
                <input
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="w-full bg-green-950/30 border border-green-800 rounded-lg pl-7 pr-3 py-2.5 text-green-300 font-mono text-sm focus:outline-none focus:border-green-500"
                  placeholder="0.00"
                />
              </div>
            </div>

            {/* Payment method */}
            <div>
              <div className="text-green-600 text-xs font-mono mb-2 tracking-widest">
                PAYMENT METHOD
              </div>
              <div className="grid grid-cols-3 gap-2">
                {[
                  ["card", "💳 CARD"],
                  ["bank", "🏦 ACH"],
                  ["crypto", "₿ CRYPTO"],
                ].map(([m, l]) => (
                  <button
                    key={m}
                    onClick={() => setMethod(m)}
                    className={`border rounded-lg py-2 text-xs font-mono transition-colors ${
                      method === m
                        ? "border-green-500 bg-green-950 text-green-300"
                        : "border-green-900 text-green-600 hover:border-green-700"
                    }`}
                  >
                    {l}
                  </button>
                ))}
              </div>
            </div>

            {/* Submit button */}
            <button className="w-full bg-green-500 hover:bg-green-400 text-black font-mono font-bold py-3 rounded-lg transition-colors tracking-widest text-sm">
              {tab === "deposit" ? "FUND AGENT →" : "WITHDRAW FUNDS →"}
            </button>

            {/* Processing times */}
            <p className="text-green-800 text-xs font-mono text-center">
              Processing time: instant (card) · 1-3 days (ACH) · 10 min (crypto)
            </p>
          </div>
        </div>

        {/* Transaction history */}
        <div className="border border-green-900 rounded-xl bg-black overflow-hidden">
          <div className="px-4 py-3 border-b border-green-900">
            <span className="text-green-500 font-mono text-xs tracking-widest">
              TRANSACTION HISTORY
            </span>
          </div>
          <div className="divide-y divide-green-950">
            {TRANSACTION_HISTORY.map((tx, i) => (
              <div
                key={i}
                className="flex items-center gap-3 px-4 py-3 hover:bg-green-950/20"
              >
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm ${
                    tx.amount > 0
                      ? "bg-green-950 text-green-400"
                      : "bg-red-950 text-red-400"
                  }`}
                >
                  {tx.amount > 0 ? "↓" : "↑"}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-green-300 font-mono text-xs font-bold">
                    {tx.type}
                  </div>
                  <div className="text-green-700 text-xs font-mono truncate">
                    {tx.hash !== "auto" ? tx.hash : "automated"} · {tx.date}
                  </div>
                </div>
                <div
                  className={`font-mono text-sm font-bold ${
                    tx.amount > 0 ? "text-green-400" : "text-red-400"
                  }`}
                >
                  {tx.amount > 0 ? "+" : ""}
                  {fmtUSD(tx.amount)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
