import React, { useState } from "react";
import { ScanlineOverlay } from "../Common";
import { KYC_STEPS } from "../../utils/constants";

/**
 * KYCPage - Know Your Customer verification flow
 * 4-step process: Personal Info → Identity Doc → Selfie → Risk Profile
 * Regulatory compliance for trading platform
 */
export function KYCPage({ onComplete }) {
  const [step, setStep] = useState(0);
  const [uploading, setUploading] = useState(false);

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      setUploading(true);
      setTimeout(() => {
        setUploading(false);
        onComplete();
      }, 2000);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4 relative">
      <ScanlineOverlay />
      
      {/* Grid background */}
      <div
        className="absolute inset-0 opacity-[0.06]"
        style={{
          backgroundImage: "linear-gradient(#0f2 1px,transparent 1px),linear-gradient(90deg,#0f2 1px,transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />

      <div className="w-full max-w-lg relative">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="text-green-400 font-mono text-2xl font-bold">KYC VERIFICATION</div>
          <div className="text-green-700 text-xs font-mono mt-1">REGULATORY COMPLIANCE · SEC/FINRA</div>
        </div>

        {/* Progress bar */}
        <div className="flex items-center mb-8">
          {KYC_STEPS.map((s, i) => (
            <div key={i} className="flex-1 flex items-center">
              <div
                className={`flex items-center justify-center w-7 h-7 rounded-full border font-mono text-xs font-bold transition-colors ${
                  i < step
                    ? "bg-green-500 border-green-500 text-black"
                    : i === step
                    ? "border-green-400 text-green-400"
                    : "border-green-900 text-green-800"
                }`}
              >
                {i < step ? "✓" : i + 1}
              </div>
              {i < 3 && (
                <div className={`flex-1 h-px ${i < step ? "bg-green-500" : "bg-green-900"}`} />
              )}
            </div>
          ))}
        </div>

        {/* Form card */}
        <div className="border border-green-800 rounded-xl bg-black/80 p-6">
          <div className="text-green-400 font-mono text-sm mb-1 uppercase tracking-widest">
            {KYC_STEPS[step]}
          </div>
          <div className="text-green-700 text-xs font-mono mb-6">
            Step {step + 1} of {KYC_STEPS.length}
          </div>

          {/* Step 0: Personal Info */}
          {step === 0 && (
            <div className="space-y-4">
              {[
                ["LEGAL FIRST NAME", "John"],
                ["LEGAL LAST NAME", "Doe"],
                ["DATE OF BIRTH", "MM/DD/YYYY"],
                ["NATIONALITY", "United States"],
                ["TAX ID / SSN", "XXX-XX-XXXX"],
              ].map(([label, ph]) => (
                <div key={label}>
                  <label className="block text-green-600 text-xs font-mono mb-1 tracking-widest">
                    {label}
                  </label>
                  <input
                    className="w-full bg-green-950/30 border border-green-800 rounded-lg px-3 py-2.5 text-green-300 font-mono text-sm focus:outline-none focus:border-green-500"
                    placeholder={ph}
                  />
                </div>
              ))}
            </div>
          )}

          {/* Step 1: Identity Document */}
          {step === 1 && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {["PASSPORT", "DRIVER LICENSE", "NATIONAL ID", "RESIDENCE PERMIT"].map(
                  (t) => (
                    <button
                      key={t}
                      className="border border-green-800 rounded-lg p-4 text-center hover:border-green-500 hover:bg-green-950/30 transition-colors"
                    >
                      <div className="text-2xl mb-1">📄</div>
                      <div className="text-green-500 text-xs font-mono">{t}</div>
                    </button>
                  )
                )}
              </div>
              <div className="border-2 border-dashed border-green-800 rounded-xl p-8 text-center hover:border-green-600 transition-colors cursor-pointer">
                <div className="text-3xl mb-2">⬆</div>
                <div className="text-green-500 font-mono text-sm">UPLOAD DOCUMENT</div>
                <div className="text-green-800 font-mono text-xs mt-1">PNG, JPG, PDF · MAX 10MB</div>
              </div>
            </div>
          )}

          {/* Step 2: Selfie Verification */}
          {step === 2 && (
            <div className="space-y-4">
              <div className="border-2 border-dashed border-green-800 rounded-xl p-12 text-center">
                <div className="w-20 h-20 rounded-full border-2 border-green-700 mx-auto mb-4 flex items-center justify-center text-3xl">
                  👤
                </div>
                <div className="text-green-500 font-mono text-sm">TAKE SELFIE</div>
                <div className="text-green-800 font-mono text-xs mt-1">Position face within frame</div>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center text-xs font-mono text-green-700">
                <div className="border border-green-900 rounded p-2">✓ Good lighting</div>
                <div className="border border-green-900 rounded p-2">✓ Face centered</div>
                <div className="border border-green-900 rounded p-2">✓ No glasses</div>
              </div>
            </div>
          )}

          {/* Step 3: Risk Profile */}
          {step === 3 && (
            <div className="space-y-4">
              {[
                ["INVESTMENT EXPERIENCE", ["Beginner", "Intermediate", "Expert"]],
                ["ANNUAL INCOME", ["< $50K", "$50K–$100K", "$100K–$500K", "> $500K"]],
                ["RISK TOLERANCE", ["Conservative", "Moderate", "Aggressive"]],
              ].map(([label, opts]) => (
                <div key={label}>
                  <label className="block text-green-600 text-xs font-mono mb-1 tracking-widest">
                    {label}
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {opts.map((o) => (
                      <button
                        key={o}
                        className="border border-green-800 rounded-lg py-2 px-3 text-green-500 font-mono text-xs hover:border-green-500 hover:bg-green-950/40 transition-colors text-left"
                      >
                        {o}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Submit button */}
          <button
            onClick={handleNext}
            className="w-full mt-6 bg-green-500 hover:bg-green-400 text-black font-mono font-bold py-3 rounded-lg transition-colors tracking-widest text-sm"
          >
            {uploading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                VERIFYING IDENTITY...
              </span>
            ) : step === 3 ? (
              "SUBMIT FOR REVIEW"
            ) : (
              "CONTINUE →"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
