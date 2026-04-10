import React, { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Loader2, TrendingUp, Table2 } from 'lucide-react'

const Analytics = () => {
  const [loading, setLoading] = useState(true)
  const [trends, setTrends] = useState(null)
  const [days, setDays] = useState(1)
  const [error, setError] = useState('')
  const [view, setView] = useState('chart') // 'chart' or 'table'

  useEffect(() => {
    fetchTrends()
  }, [days])

  const fetchTrends = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await dashboardAPI.getTrends(days)
      console.log('Trends data:', response.data)
      setTrends(response.data)
    } catch (err) {
      console.error('Analytics error:', err)
      setError('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <Loader2 size={48} className="animate-spin text-green-500 mb-4" />
        <p className="text-gray-400">Loading analytics...</p>
        <p className="text-gray-500 text-sm mt-2">Fetching sensor history</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-white">Live Sensor Data</h1>
          {trends && (
            <p className="text-sm text-gray-400 mt-1">
              {trends.total_readings || 0} readings in last {days} day(s)
            </p>
          )}
        </div>
        
        <div className="flex items-center space-x-3">
          {/* Time selector */}
          <div className="flex space-x-2">
            {[1, 3, 7].map(d => (
              <button
                key={d}
                onClick={() => setDays(d)}
                className={`px-4 py-2 rounded-lg font-medium ${
                  days === d ? 'bg-green-500 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {d}D
              </button>
            ))}
          </div>

          {/* View toggle */}
          <div className="flex bg-gray-700 rounded-lg p-1">
            <button
              onClick={() => setView('chart')}
              className={`px-3 py-1.5 rounded-md flex items-center space-x-2 ${
                view === 'chart' ? 'bg-green-500 text-white' : 'text-gray-300'
              }`}
            >
              <TrendingUp size={16} />
              <span>Chart</span>
            </button>
            <button
              onClick={() => setView('table')}
              className={`px-3 py-1.5 rounded-md flex items-center space-x-2 ${
                view === 'table' ? 'bg-green-500 text-white' : 'text-gray-300'
              }`}
            >
              <Table2 size={16} />
              <span>Table</span>
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded-lg text-red-200">
          {error}
        </div>
      )}

      {trends && trends.sensor_trend && trends.sensor_trend.length > 0 ? (
        <>
          {view === 'chart' ? (
            <div className="card mb-6">
              <h3 className="text-lg font-semibold text-white mb-4">Sensor Trends</h3>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={trends.sensor_trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis
                    dataKey="timestamp"
                    stroke="#9CA3AF"
                    tick={{fill: '#9CA3AF', fontSize: 12}}
                    tickFormatter={(val) => new Date(val).toLocaleTimeString()}
                  />
                  <YAxis stroke="#9CA3AF" tick={{fill: '#9CA3AF', fontSize: 12}} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '8px' }}
                    labelStyle={{ color: '#FFF' }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="temperature" stroke="#EF4444" strokeWidth={2} name="Temp (C)" dot={false} />
                  <Line type="monotone" dataKey="humidity" stroke="#3B82F6" strokeWidth={2} name="Humidity (%)" dot={false} />
                  <Line type="monotone" dataKey="soil_moisture" stroke="#10B981" strokeWidth={2} name="Soil (ADC)" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="card mb-6 overflow-x-auto">
              <h3 className="text-lg font-semibold text-white mb-4">Sensor Readings Table</h3>
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="pb-3 text-gray-400 font-medium">Time</th>
                    <th className="pb-3 text-gray-400 font-medium">Temp (C)</th>
                    <th className="pb-3 text-gray-400 font-medium">Humidity (%)</th>
                    <th className="pb-3 text-gray-400 font-medium">Soil (ADC)</th>
                  </tr>
                </thead>
                <tbody>
                  {trends.sensor_trend.slice(-50).reverse().map((row, i) => (
                    <tr key={i} className="border-b border-gray-800 hover:bg-gray-800/50">
                      <td className="py-3 text-gray-300">{new Date(row.timestamp).toLocaleString()}</td>
                      <td className="py-3 text-red-400 font-medium">{row.temperature}</td>
                      <td className="py-3 text-blue-400 font-medium">{row.humidity}</td>
                      <td className="py-3 text-green-400 font-medium">{row.soil_moisture}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      ) : (
        <div className="card text-center py-12">
          <p className="text-gray-400 text-lg mb-2">No sensor data for this period</p>
          <p className="text-gray-500 mb-4">Make sure Arduino is connected and sending data</p>
          <div className="space-x-4">
            <button onClick={fetchTrends} className="btn-secondary">
              Retry
            </button>
            <button onClick={() => window.open('http://localhost:5173/dashboard', '_self')} className="btn-primary">
              Go to Dashboard
            </button>
          </div>
          <div className="mt-8 text-sm text-gray-600 dark:text-gray-400">
            <p>Troubleshooting:</p>
            <ul className="mt-2 space-y-1">
              <li>✓ Check if USB bridge is running in another terminal</li>
              <li>✓ Verify backend is accessible at http://localhost:8000</li>
              <li>✓ Try selecting a different time period (1D, 3D, 7D)</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

export default Analytics
