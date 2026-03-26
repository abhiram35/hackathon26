import React, { useState } from "react";
import { ScanlineOverlay, TerminalLine } from "../Common";

/**
 * LoginPage - Authentication entry point
 * Handles both login and signup modes
 * Features: Email/password auth, OAuth options, loading states
 */
export function LoginPage({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = () => {
    setLoading(true);
    setTimeout(() => { 
      setLoading(false); 
      onLogin(email || "trader@apex.ai"); 
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center relative overflow-hidden">
      <ScanlineOverlay />
      
      {/* Grid background */}
      <div
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: "linear-gradient(#0f2 1px,transparent 1px),linear-gradient(90deg,#0f2 1px,transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />
      
      {/* Glow effect */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-green-500/5 blur-3xl pointer-events-none" />

      <div className="relative w-full max-w-md mx-4">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="text-5xl font-mono font-black text-green-400 tracking-tight">
            ◈ APEX
          </div>
          <div className="text-green-600 font-mono text-sm tracking-[0.4em] mt-1">
            REINFORCEMENT TRADING
          </div>
          <div className="mt-3 flex justify-center gap-2">
            {["BUY", "HOLD", "SELL"].map((t) => (
              <span 
                key={t} 
                className="text-xs font-mono px-2 py-0.5 border border-green-900 text-green-700 rounded"
              >
                {t}
              </span>
            ))}
          </div>
        </div>

        {/* Login card */}
        <div className="border border-green-800 rounded-xl bg-black/80 p-8 backdrop-blur">
          {/* Mode tabs */}
          <div className="flex mb-6 border border-green-900 rounded-lg overflow-hidden">
            {["login", "signup"].map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={`flex-1 py-2 text-xs font-mono uppercase tracking-widest transition-colors ${
                  mode === m ? "bg-green-900 text-green-300" : "text-green-700 hover:text-green-500"
                }`}
              >
                {m}
              </button>
            ))}
          </div>

          <div className="space-y-4">
            {/* Full name field (signup only) */}
            {mode === "signup" && (
              <div>
                <label className="block text-green-600 text-xs font-mono mb-1 tracking-widest">
                  FULL NAME
                </label>
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-green-950/30 border border-green-800 rounded-lg px-3 py-2.5 text-green-300 font-mono text-sm focus:outline-none focus:border-green-500 transition-colors"
                  placeholder="John Doe"
                />
              </div>
            )}

            {/* Email field */}
            <div>
              <label className="block text-green-600 text-xs font-mono mb-1 tracking-widest">
                EMAIL
              </label>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-green-950/30 border border-green-800 rounded-lg px-3 py-2.5 text-green-300 font-mono text-sm focus:outline-none focus:border-green-500 transition-colors"
                placeholder="trader@apex.ai"
              />
            </div>

            {/* Password field */}
            <div>
              <label className="block text-green-600 text-xs font-mono mb-1 tracking-widest">
                PASSWORD
              </label>
              <input
                type="password"
                value={pass}
                onChange={(e) => setPass(e.target.value)}
                className="w-full bg-green-950/30 border border-green-800 rounded-lg px-3 py-2.5 text-green-300 font-mono text-sm focus:outline-none focus:border-green-500 transition-colors"
                placeholder="••••••••"
              />
            </div>

            {/* Forgot password link (login only) */}
            {mode === "login" && (
              <div className="text-right">
                <button className="text-green-600 text-xs font-mono hover:text-green-400 transition-colors">
                  FORGOT PASSWORD?
                </button>
              </div>
            )}

            {/* Submit button */}
            <button
              onClick={handleSubmit}
              className="w-full bg-green-500 hover:bg-green-400 text-black font-mono font-bold py-3 rounded-lg transition-colors tracking-widest text-sm relative overflow-hidden"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                  AUTHENTICATING...
                </span>
              ) : (
                mode === "login" ? "ENTER THE MARKET" : "CREATE ACCOUNT"
              )}
            </button>

            {/* Terms (signup only) */}
            {mode === "signup" && (
              <p className="text-green-800 text-xs font-mono text-center leading-relaxed">
                By signing up you agree to our Terms of Service and acknowledge you understand autonomous trading risks.
              </p>
            )}
          </div>

          {/* OAuth options */}
          <div className="mt-4 pt-4 border-t border-green-900">
            <div className="text-center text-green-700 text-xs font-mono mb-3">OR CONTINUE WITH</div>
            <div className="grid grid-cols-2 gap-3">
              {["◎ GOOGLE", "⬡ GITHUB"].map((s) => (
                <button 
                  key={s} 
                  onClick={handleSubmit} 
                  className="border border-green-900 rounded-lg py-2 text-green-600 font-mono text-xs hover:border-green-700 hover:text-green-400 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-4 text-center">
          <TerminalLine text="Initializing RL trading engine..." delay={500} />
        </div>
      </div>
    </div>
  );
}
