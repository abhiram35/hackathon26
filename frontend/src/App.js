import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import TrainingControl from './components/TrainingControl';
import SessionList from './components/SessionList';

function App() {
  const [healthStatus, setHealthStatus] = useState('loading');
  const [sessions, setSessions] = useState([]);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    checkHealth();
    fetchSessions();
    // Refresh sessions every 5 seconds
    const interval = setInterval(fetchSessions, 5000);
    return () => clearInterval(interval);
  }, [refreshTrigger]);

  const checkHealth = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      setHealthStatus(data.status);
    } catch (error) {
      setHealthStatus('error');
      console.error('Health check failed:', error);
    }
  };

  const fetchSessions = async () => {
    try {
      const response = await fetch('http://localhost:8000/sessions');
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error('Failed to fetch sessions:', error);
    }
  };

  const handleTrainingComplete = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              📈 RL Trading Agent
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-sm font-medium text-gray-600">Status:</div>
            {healthStatus === 'healthy' ? (
              <div className="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-full border border-green-200">
                <div className="w-2 h-2 bg-green-600 rounded-full animate-pulse"></div>
                🟢 Online
              </div>
            ) : healthStatus === 'loading' ? (
              <div className="flex items-center gap-2 px-4 py-2 bg-yellow-50 text-yellow-700 rounded-full border border-yellow-200">
                <div className="w-2 h-2 bg-yellow-600 rounded-full pulse-custom"></div>
                ⏳ Connecting...
              </div>
            ) : (
              <div className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-700 rounded-full border border-red-200">
                <div className="w-2 h-2 bg-red-600 rounded-full"></div>
                🔴 Offline
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Training Control */}
          <div className="fade-in">
            <TrainingControl onTrainingComplete={handleTrainingComplete} />
          </div>

          {/* Dashboard */}
          <div className="fade-in">
            <Dashboard sessions={sessions} />
          </div>
        </div>

        {/* Sessions List */}
        <div className="fade-in">
          <SessionList sessions={sessions} onRefresh={handleTrainingComplete} />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-gray-600">
          <p>RL Trading Agent Dashboard • Powered by FastAPI & React</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
