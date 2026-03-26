import React, { useState } from "react";
import { LoginPage, KYCPage } from "./components/Auth";
import {
  HomePage,
  PortfolioPage,
  DashboardPage,
  DiscoverPage,
  WalletPage,
} from "./components/Pages";
import { Sidebar, Topbar } from "./components/Layout";
import { ScanlineOverlay } from "./components/Common";

/**
 * Main App Component
 * Handles authentication flow and page routing
 * - LOGIN: Initial authentication
 * - KYC: Know Your Customer verification
 * - APP: Main trading dashboard with 5 pages
 */
export default function App() {
  const [authState, setAuthState] = useState("login"); // login | kyc | app
  const [page, setPage] = useState("home");
  const [user, setUser] = useState("");

  // Authentication flow: login -> kyc -> app
  if (authState === "login") {
    return (
      <LoginPage
        onLogin={(email) => {
          setUser(email);
          setAuthState("kyc");
        }}
      />
    );
  }

  if (authState === "kyc") {
    return <KYCPage onComplete={() => setAuthState("app")} />;
  }

  // Main app with navigation and pages
  const pages = {
    home: <HomePage setPage={setPage} />,
    portfolio: <PortfolioPage />,
    dashboard: <DashboardPage />,
    discover: <DiscoverPage />,
    wallet: <WalletPage />,
  };

  return (
    <div className="min-h-screen bg-black text-green-300">
      <ScanlineOverlay />

      {/* Global styles */}
      <style>{`
        body { 
          background: #000; 
          margin: 0;
          padding: 0;
        }
        ::-webkit-scrollbar { 
          width: 4px; 
          height: 4px; 
        }
        ::-webkit-scrollbar-track { 
          background: #000; 
        }
        ::-webkit-scrollbar-thumb { 
          background: #14532d; 
          border-radius: 2px; 
        }
        * { 
          box-sizing: border-box; 
        }
      `}</style>

      {/* Layout components */}
      <Sidebar page={page} setPage={setPage} />
      <Topbar user={user} />

      {/* Main content area */}
      <main className="ml-16 md:ml-56 pt-12 min-h-screen">
        <div className="p-4 md:p-6 max-w-7xl">
          {pages[page]}
        </div>
      </main>
    </div>
  );
}
