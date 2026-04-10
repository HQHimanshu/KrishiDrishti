import React, { useState } from 'react'
import { Send, Loader2, MessageSquare } from 'lucide-react'
import { adviceAPI } from '../../services/api'
import AdviceCard from './AdviceCard'

const ChatInterface = () => {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [advice, setAdvice] = useState(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    setError('')
    setAdvice(null)

    try {
      const response = await adviceAPI.getAdvice(question, null)
      setAdvice(response.data)
      setQuestion('')
    } catch (err) {
      console.error('Chat error:', err.response?.data || err.message)
      
      if (err.response?.status === 500) {
        setError('❌ Qwen model failed to load. Your system needs more RAM.\n\nFix: Run "ollama pull qwen2.5:1.5b" then update .env to OLLAMA_MODEL=qwen2.5:1.5b')
      } else if (err.response?.status === 503) {
        setError('🤖 Ollama is not running. Open terminal and run: ollama serve')
      } else {
        setError(`Failed: ${err.response?.data?.detail || err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  const suggestions = [
    "Should I irrigate now based on current soil moisture?",
    "What fertilizer should I use for wheat?",
    "What is photosynthesis?",
    "How to improve crop yield?"
  ]

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
        <MessageSquare size={20} />
        <span>AI Assistant (Qwen 2.5)</span>
      </h3>

      <div className="bg-gray-50 dark:bg-gray-900/50 rounded-lg p-4 mb-4 min-h-[300px] max-h-[500px] overflow-y-auto">
        {!advice && !loading && !error && (
          <div className="text-center text-gray-600 dark:text-gray-400 py-12">
            <MessageSquare size={48} className="mx-auto mb-4 opacity-50" />
            <p className="mb-4">Ask any question!</p>
            <div className="space-y-2">
              {suggestions.map((q, i) => (
                <button
                  key={i}
                  onClick={() => setQuestion(q)}
                  className="block w-full text-left px-4 py-2 bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg text-gray-700 dark:text-gray-300 text-sm transition-colors border border-gray-200 dark:border-gray-700"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 size={32} className="animate-spin text-green-500" />
            <span className="ml-3 text-gray-600 dark:text-gray-400">Thinking...</span>
          </div>
        )}

        {advice && <AdviceCard advice={advice} />}
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/50 border border-red-300 dark:border-red-700 rounded-lg text-red-700 dark:text-red-200 text-sm whitespace-pre-line">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask anything..."
          className="flex-1 px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  )
}

export default ChatInterface
