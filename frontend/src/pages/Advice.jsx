import React, { useState, useEffect } from 'react'
import { adviceAPI } from '../services/api'
import ChatInterface from '../components/ai/ChatInterface'
import AdviceCard from '../components/ai/AdviceCard'
import { Loader2, MessageSquare, History } from 'lucide-react'
import { timeAgo } from '../utils/formatters'

const Advice = () => {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [showHistory, setShowHistory] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await adviceAPI.getHistory(10)
      setHistory(response.data)
    } catch (err) {
      setError('Failed to load advice history')
      console.error('History error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-white flex items-center space-x-2">
          <MessageSquare size={32} />
          <span>AI Farming Advice</span>
        </h1>
        <button
          onClick={() => setShowHistory(!showHistory)}
          className="btn-secondary flex items-center space-x-2"
        >
          <History size={18} />
          <span>{showHistory ? 'Show Chat' : 'History'}</span>
        </button>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Chat Interface */}
        <ChatInterface />

        {/* History or Advice Card */}
        {showHistory ? (
          <div className="card">
            <h3 className="text-lg font-semibold text-white mb-4">📜 Advice History</h3>
            {loading ? (
              <div className="flex justify-center py-8">
                <Loader2 size={32} className="animate-spin text-primary-500" />
              </div>
            ) : error ? (
              <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-200">
                {error}
              </div>
            ) : history.length === 0 ? (
              <div className="text-gray-400 text-center py-8">No history yet. Ask a question in the chat!</div>
            ) : (
              <div className="space-y-3 max-h-[500px] overflow-y-auto">
                {history.map((item) => (
                  <div
                    key={item.id}
                    className="bg-gray-700/50 rounded-lg p-4 hover:bg-gray-700 cursor-pointer transition-colors"
                  >
                    <div className="text-white font-medium mb-1">{item.question}</div>
                    <div className="text-gray-400 text-sm line-clamp-2">{item.answer}</div>
                    <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                      <span className={`px-2 py-1 rounded ${
                        item.recommendation_type === 'IRRIGATE'
                          ? 'bg-blue-900 text-blue-200'
                          : item.recommendation_type === 'WAIT'
                          ? 'bg-yellow-900 text-yellow-200'
                          : 'bg-green-900 text-green-200'
                      }`}>
                        {item.recommendation_type || 'N/A'}
                      </span>
                      <span>{timeAgo(item.timestamp)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="card">
            <h3 className="text-lg font-semibold text-white mb-4">💡 Quick Tips</h3>
            <div className="space-y-4 text-gray-300">
              <div className="bg-blue-900/30 rounded-lg p-4">
                <h4 className="font-semibold text-blue-300 mb-2">💧 Irrigation Tips</h4>
                <ul className="text-sm space-y-1 list-disc list-inside">
                  <li>Irrigate early morning or evening</li>
                  <li>Check soil moisture before watering</li>
                  <li>Use drip irrigation to save water</li>
                </ul>
              </div>
              <div className="bg-green-900/30 rounded-lg p-4">
                <h4 className="font-semibold text-green-300 mb-2">🌱 Crop Care</h4>
                <ul className="text-sm space-y-1 list-disc list-inside">
                  <li>Monitor pH levels regularly</li>
                  <li>Use organic fertilizers when possible</li>
                  <li>Watch for pest signs in weather changes</li>
                </ul>
              </div>
              <div className="bg-amber-900/30 rounded-lg p-4">
                <h4 className="font-semibold text-amber-300 mb-2">🌦️ Weather Alerts</h4>
                <ul className="text-sm space-y-1 list-disc list-inside">
                  <li>Check forecast before applying fertilizer</li>
                  <li>Protect crops from extreme heat</li>
                  <li>Prepare drainage for heavy rain</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Advice
