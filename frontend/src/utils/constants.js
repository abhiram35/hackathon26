/**
 * Constants for RL Trading App
 * Stock data, portfolio holdings, and live trades
 */

export const STOCKS = {
  top10: [
    { sym: "NVDA", name: "NVIDIA Corp", price: 872.4, change: 3.21, mktCap: "2.14T", sector: "Tech" },
    { sym: "AAPL", name: "Apple Inc", price: 189.3, change: 1.05, mktCap: "2.93T", sector: "Tech" },
    { sym: "MSFT", name: "Microsoft", price: 418.7, change: 0.87, mktCap: "3.11T", sector: "Tech" },
    { sym: "GOOGL", name: "Alphabet", price: 175.2, change: 2.14, mktCap: "2.17T", sector: "Tech" },
    { sym: "META", name: "Meta Platforms", price: 503.1, change: 1.78, mktCap: "1.29T", sector: "Tech" },
    { sym: "AMZN", name: "Amazon", price: 186.4, change: 0.64, mktCap: "1.96T", sector: "Commerce" },
    { sym: "TSLA", name: "Tesla Inc", price: 246.8, change: -1.2, mktCap: "0.79T", sector: "EV" },
    { sym: "BRK", name: "Berkshire H.", price: 380.5, change: 0.31, mktCap: "0.83T", sector: "Finance" },
    { sym: "JPM", name: "JPMorgan Chase", price: 198.7, change: 0.52, mktCap: "0.58T", sector: "Finance" },
    { sym: "V", name: "Visa Inc", price: 276.3, change: 0.78, mktCap: "0.57T", sector: "Finance" },
  ],
  profitable: [
    { sym: "LLY", name: "Eli Lilly", price: 743.2, change: 4.87, mktCap: "0.71T", sector: "Pharma" },
    { sym: "SMCI", name: "Super Micro", price: 812.5, change: 6.23, mktCap: "0.048T", sector: "Hardware" },
    { sym: "ARM", name: "Arm Holdings", price: 135.6, change: 5.14, mktCap: "0.14T", sector: "Semicon" },
    { sym: "PLTR", name: "Palantir", price: 24.3, change: 3.97, mktCap: "0.052T", sector: "AI" },
    { sym: "MSTR", name: "MicroStrategy", price: 1640.0, change: 8.12, mktCap: "0.029T", sector: "Crypto" },
  ],
  upcoming: [
    { sym: "LUNR", name: "Intuitive Mach.", price: 12.4, change: 14.3, mktCap: "1.4B", sector: "Space" },
    { sym: "IONQ", name: "IonQ Inc", price: 19.8, change: 9.7, mktCap: "3.2B", sector: "Quantum" },
    { sym: "RKLB", name: "Rocket Lab", price: 8.7, change: 7.2, mktCap: "4.1B", sector: "Space" },
    { sym: "ACHR", name: "Archer Aviation", price: 6.3, change: 11.4, mktCap: "1.9B", sector: "eVTOL" },
    { sym: "DNA", name: "Ginkgo Bioworks", price: 2.1, change: 5.9, mktCap: "0.8B", sector: "BioTech" },
  ],
  highRisk: [
    { sym: "BBAI", name: "BigBear.ai", price: 3.8, change: -12.4, mktCap: "0.6B", sector: "AI" },
    { sym: "NKLA", name: "Nikola Corp", price: 0.9, change: -18.7, mktCap: "0.2B", sector: "EV" },
    { sym: "FFIE", name: "Faraday Future", price: 0.4, change: 22.1, mktCap: "0.1B", sector: "EV" },
    { sym: "BYND", name: "Beyond Meat", price: 7.2, change: -9.8, mktCap: "0.45B", sector: "Food" },
    { sym: "SPCE", name: "Virgin Galactic", price: 1.6, change: -15.3, mktCap: "0.31B", sector: "Space" },
  ],
};

export const LIVE_TRADES = [
  { id: 1, sym: "NVDA", action: "BUY", qty: 12, price: 871.2, time: "14:32:01", pnl: +143.6, status: "FILLED" },
  { id: 2, sym: "AAPL", action: "SELL", qty: 30, price: 189.8, time: "14:31:47", pnl: +67.2, status: "FILLED" },
  { id: 3, sym: "TSLA", action: "BUY", qty: 8, price: 247.1, time: "14:31:22", pnl: -23.4, status: "PARTIAL" },
  { id: 4, sym: "META", action: "SELL", qty: 5, price: 502.6, time: "14:30:55", pnl: +89.5, status: "FILLED" },
  { id: 5, sym: "MSFT", action: "BUY", qty: 15, price: 417.9, time: "14:30:31", pnl: +201.3, status: "FILLED" },
  { id: 6, sym: "LLY", action: "BUY", qty: 3, price: 741.0, time: "14:29:58", pnl: +66.6, status: "FILLED" },
];

export const PORTFOLIO_HOLDINGS = [
  { sym: "NVDA", qty: 42, avgCost: 831.2, currPrice: 872.4, pnl: 1730.4 },
  { sym: "AAPL", qty: 120, avgCost: 175.4, currPrice: 189.3, pnl: 1668.0 },
  { sym: "MSFT", qty: 30, avgCost: 401.0, currPrice: 418.7, pnl: 531.0 },
  { sym: "META", qty: 18, avgCost: 480.2, currPrice: 503.1, pnl: 412.2 },
  { sym: "TSLA", qty: 25, avgCost: 251.4, currPrice: 246.8, pnl: -115.0 },
  { sym: "LLY", qty: 7, avgCost: 710.0, currPrice: 743.2, pnl: 232.4 },
];

export const NAV_ITEMS = [
  { id: "home", label: "HOME", icon: "⬡" },
  { id: "portfolio", label: "PORTFOLIO", icon: "◈" },
  { id: "dashboard", label: "DASHBOARD", icon: "▦" },
  { id: "discover", label: "DISCOVER", icon: "◉" },
  { id: "wallet", label: "WALLET", icon: "◆" },
];

export const KYC_STEPS = ["Personal Info", "Identity Doc", "Selfie Verify", "Risk Profile"];

export const TRANSACTION_HISTORY = [
  { type: "DEPOSIT", amount: 10000, date: "2024-11-28", status: "CONFIRMED", hash: "0x1a2b...c3d4" },
  { type: "AGENT PROFIT", amount: 1247.8, date: "2024-11-27", status: "CONFIRMED", hash: "auto" },
  { type: "WITHDRAW", amount: -2500, date: "2024-11-25", status: "CONFIRMED", hash: "0x9f8e...7d6c" },
  { type: "DEPOSIT", amount: 5000, date: "2024-11-20", status: "CONFIRMED", hash: "0x5a4b...2c1d" },
  { type: "AGENT PROFIT", amount: 892.4, date: "2024-11-19", status: "CONFIRMED", hash: "auto" },
];

export const HOME_STATS = [
  { label: "TOTAL AUM", value: "$4.82M", sub: "+2.14% today", positive: true, icon: "◆" },
  { label: "TODAY'S PROFIT", value: "+$9,412", sub: "127 trades executed", positive: true, icon: "▲" },
  { label: "WIN RATE", value: "73.4%", sub: "Last 30 days", positive: true, icon: "◉" },
  { label: "SHARPE RATIO", value: "2.87", sub: "Annualized", positive: true, icon: "≋" },
];
