import React, { useState, useEffect } from 'react'

// API_BASE_URL is the backend FastAPI server URL, not a model endpoint.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002'

const HistoryPanel = ({ userName, isVisible, onToggle }) => {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchHistory = async () => {
    if (!userName) return
    
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/history/${userName}`)
      const data = await response.json()
      setHistory(data.history || [])
    } catch (error) {
      console.error('Failed to fetch history:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (isVisible && userName) {
      fetchHistory()
    }
  }, [isVisible, userName])

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  if (!isVisible) return null

  return (
    <div className="fixed right-4 top-20 w-80 bg-white rounded-2xl shadow-2xl border border-gray-100 z-50 animate-slideIn">
      <div className="flex items-center justify-between p-6 border-b border-gray-100 bg-gradient-to-r from-blue-500 to-purple-600 rounded-t-2xl">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3">
            <span className="text-white">📚</span>
          </div>
          <h3 className="font-semibold text-white text-lg">Chat History</h3>
        </div>
        <button
          onClick={onToggle}
          className="text-white hover:text-gray-200 transition-colors p-1 rounded-full hover:bg-white hover:bg-opacity-20"
        >
          <span className="text-xl">✕</span>
        </button>
      </div>
      
      <div className="max-h-96 overflow-y-auto p-4">
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <div className="text-gray-500">Loading history...</div>
          </div>
        ) : history.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-6xl mb-4">🤔</div>
            <div className="text-gray-500">No conversation history yet</div>
            <div className="text-sm text-gray-400 mt-2">Start chatting to see your history!</div>
          </div>
        ) : (
          <div className="space-y-3">
            {history.map((entry, index) => (
              <div
                key={index}
                className={`p-4 rounded-xl transition-all duration-200 hover:scale-[1.02] ${
                  entry.sender === 'user'
                    ? 'bg-gradient-to-r from-blue-50 to-indigo-50 ml-2 border-l-4 border-blue-500'
                    : 'bg-gradient-to-r from-gray-50 to-gray-100 mr-2 border-l-4 border-purple-500'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className={`text-xs font-semibold ${
                    entry.sender === 'user' ? 'text-blue-600' : 'text-purple-600'
                  }`}>
                    {entry.sender === 'user' ? '👤 You' : '🤖 AI Tutor'}
                  </div>
                  <div className="text-xs text-gray-400">
                    {formatTime(entry.timestamp)}
                  </div>
                </div>
                <div className="text-sm text-gray-700 line-clamp-3">
                  {entry.message}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {userName && (
        <div className="p-4 border-t border-gray-100 bg-gray-50 rounded-b-2xl">
          <button
            onClick={fetchHistory}
            className="w-full px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            <span className="flex items-center justify-center">
              🔄 <span className="ml-2">Refresh History</span>
            </span>
          </button>
        </div>
      )}
    </div>
  )
}

export default HistoryPanel
