import React, { useState } from 'react';

function TrainingControl({ onTrainingComplete }) {
  const [loading, setLoading] = useState(false);
  const [priceData, setPriceData] = useState('');
  const [timesteps, setTimesteps] = useState(10000);
  const [balance, setBalance] = useState(10000);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' or 'error'

  const handleTrain = async (e) => {
    e.preventDefault();
    
    if (!priceData.trim()) {
      setMessage('Please enter price data');
      setMessageType('error');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const prices = priceData.trim().split(',').map(p => parseFloat(p.trim()));
      
      if (prices.some(isNaN)) {
        setMessage('Invalid price data. Please enter numbers separated by commas.');
        setMessageType('error');
        setLoading(false);
        return;
      }

      const response = await fetch('http://localhost:8000/train', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          price_data: prices,
          total_timesteps: timesteps,
          initial_balance: balance,
          session_name: `Training ${new Date().toLocaleString()}`
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMessage(`✅ Training started! Session ID: ${data.session_id.substring(0, 8)}...`);
      setMessageType('success');
      setPriceData('');
      setTimeout(() => onTrainingComplete(), 1000);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <span className="text-2xl">🚀</span>
        Start Training
      </h2>
      <form onSubmit={handleTrain} className="space-y-4">
        {/* Price Data Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📈 Price Data (comma-separated)
          </label>
          <textarea
            value={priceData}
            onChange={(e) => setPriceData(e.target.value)}
            placeholder="100, 102, 101, 103, 105, 104, 106..."
            rows="4"
            disabled={loading}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:bg-gray-100 transition"
          />
          <p className="text-xs text-gray-500 mt-1">Enter at least 50 price points</p>
        </div>

        {/* Parameters Grid */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              ⏱️ Total Timesteps
            </label>
            <input
              type="number"
              value={timesteps}
              onChange={(e) => setTimesteps(parseInt(e.target.value))}
              min="1000"
              disabled={loading}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:bg-gray-100 transition"
            />
            <p className="text-xs text-gray-500 mt-1">Min: 1000</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              💰 Initial Balance
            </label>
            <input
              type="number"
              value={balance}
              onChange={(e) => setBalance(parseFloat(e.target.value))}
              min="100"
              disabled={loading}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:bg-gray-100 transition"
            />
            <p className="text-xs text-gray-500 mt-1">USD</p>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-semibold py-3 rounded-lg transition duration-200 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
              Training in progress...
            </>
          ) : (
            <>
              <span>🚀</span>
              Start Training
            </>
          )}
        </button>

        {/* Message Alert */}
        {message && (
          <div
            className={`p-4 rounded-lg border ${
              messageType === 'success'
                ? 'bg-green-50 border-green-200 text-green-800'
                : 'bg-red-50 border-red-200 text-red-800'
            }`}
          >
            <p className="text-sm">{message}</p>
          </div>
        )}
      </form>
    </div>
  );
}

export default TrainingControl;
