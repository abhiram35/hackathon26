import React, { useState } from 'react';

function SessionList({ sessions, onRefresh }) {
  const [expandedId, setExpandedId] = useState(null);

  const handleDelete = async (sessionId) => {
    if (!window.confirm('Delete this session?')) return;

    try {
      const response = await fetch(`http://localhost:8000/sessions/${sessionId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        onRefresh();
      }
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">✅ Completed</span>;
      case 'training':
        return <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium flex items-center gap-1"><div className="animate-spin inline-block w-3 h-3 border-2 border-yellow-600 border-t-transparent rounded-full"></div> Training</span>;
      case 'failed':
        return <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">❌ Failed</span>;
      default:
        return <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium">⏳ {status}</span>;
    }
  };

  const getReturnColor = (returnValue) => {
    if (!returnValue) return 'text-gray-600';
    return returnValue >= 0 ? 'text-green-600' : 'text-red-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
        <span className="text-2xl">📋</span>
        Training Sessions
      </h2>

      {sessions.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg mb-4">No sessions yet</p>
          <p className="text-gray-400 text-sm">Start a training session to see results here</p>
        </div>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {sessions.map(session => (
            <div
              key={session.session_id}
              className="border border-gray-200 rounded-lg hover:shadow-md transition cursor-pointer"
            >
              {/* Header / Summary */}
              <div
                onClick={() => setExpandedId(expandedId === session.session_id ? null : session.session_id)}
                className="p-4 hover:bg-gray-50 transition"
              >
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-4 flex-1">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 text-sm">
                        Session {session.session_id.substring(0, 8)}...
                      </h3>
                      <p className="text-xs text-gray-500 mt-1">
                        Created: {new Date(session.created_at).toLocaleString()}
                      </p>
                    </div>
                    {getStatusBadge(session.status)}
                  </div>
                  <div className="text-right">
                    {session.total_return !== undefined && (
                      <p className={`text-lg font-bold ${getReturnColor(session.total_return)}`}>
                        {session.total_return >= 0 ? '+' : ''}
                        {(session.total_return * 100).toFixed(2)}%
                      </p>
                    )}
                    <p className="text-xs text-gray-500">{session.num_steps} steps</p>
                  </div>
                  <span className="ml-4 text-gray-400">
                    {expandedId === session.session_id ? '▼' : '▶'}
                  </span>
                </div>
              </div>

              {/* Expanded Details */}
              {expandedId === session.session_id && (
                <div className="border-t border-gray-200 bg-gray-50 p-4 space-y-3">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600 font-medium">Created</p>
                      <p className="text-gray-900">{new Date(session.created_at).toLocaleString()}</p>
                    </div>
                    {session.completed_at && (
                      <div>
                        <p className="text-gray-600 font-medium">Completed</p>
                        <p className="text-gray-900">{new Date(session.completed_at).toLocaleString()}</p>
                      </div>
                    )}
                    <div>
                      <p className="text-gray-600 font-medium">Steps</p>
                      <p className="text-gray-900">{session.num_steps}</p>
                    </div>
                    <div>
                      <p className="text-gray-600 font-medium">Status</p>
                      <p className="text-gray-900 capitalize">{session.status}</p>
                    </div>
                  </div>

                  <button
                    onClick={() => handleDelete(session.session_id)}
                    className="w-full mt-4 px-4 py-2 bg-red-50 hover:bg-red-100 text-red-700 rounded-lg transition font-medium text-sm"
                  >
                    🗑️ Delete Session
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SessionList;
