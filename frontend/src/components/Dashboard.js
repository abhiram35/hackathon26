import React from 'react';

function Dashboard({ sessions }) {
  const completedSessions = sessions.filter(s => s.status === 'completed');
  const avgReturn = completedSessions.length > 0
    ? (completedSessions.reduce((sum, s) => sum + (s.total_return || 0), 0) / completedSessions.length * 100).toFixed(2)
    : 0;
  const successRate = sessions.length > 0 ? ((completedSessions.length / sessions.length) * 100).toFixed(0) : 0;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <span className="text-2xl">📊</span>
        Dashboard
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Sessions */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <p className="text-sm font-medium text-blue-700 mb-2">Total Sessions</p>
          <p className="text-3xl font-bold text-blue-900">{sessions.length}</p>
          <p className="text-xs text-blue-600 mt-2">All time</p>
        </div>

        {/* Completed Sessions */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
          <p className="text-sm font-medium text-green-700 mb-2">Completed</p>
          <p className="text-3xl font-bold text-green-900">{completedSessions.length}</p>
          <p className="text-xs text-green-600 mt-2">Finished runs</p>
        </div>

        {/* Average Return */}
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
          <p className="text-sm font-medium text-purple-700 mb-2">Avg Return</p>
          <p className={`text-3xl font-bold ${avgReturn >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {avgReturn}%
          </p>
          <p className="text-xs text-purple-600 mt-2">Average</p>
        </div>

        {/* Success Rate */}
        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-4 border border-orange-200">
          <p className="text-sm font-medium text-orange-700 mb-2">Success Rate</p>
          <p className="text-3xl font-bold text-orange-900">{successRate}%</p>
          <p className="text-xs text-orange-600 mt-2">Completion rate</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
