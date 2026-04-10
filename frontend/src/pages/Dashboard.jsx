import React, { useState, useEffect } from 'react'
import { dashboardAPI, sensorAPI } from '../services/api'
import SensorGrid from '../components/dashboard/SensorGrid'
import WeatherWidget from '../components/dashboard/WeatherWidget'
import ResourceMetrics from '../components/dashboard/ResourceMetrics'
import QuickActions from '../components/dashboard/QuickActions'
import AlertList from '../components/notifications/AlertList'
import { Loader2 } from 'lucide-react'

const Dashboard = () => {
  const [loading, setLoading] = useState(true)
  const [metrics, setMetrics] = useState(null)
  const [error, setError] = useState('')
  const [lastUpdate, setLastUpdate] = useState(null)
  const [debug, setDebug] = useState(false)

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchMetrics = async () => {
    try {
      const response = await dashboardAPI.getMetrics()
      console.log('Dashboard data:', response.data)
      setMetrics(response.data)
      setLastUpdate(new Date())
      if (loading) setLoading(false)
    } catch (err) {
      console.error('Dashboard error:', err.response?.data || err.message)
      setError(err.response?.data?.detail || 'Failed to connect to backend')
      if (loading) setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <Loader2 size={48} className="animate-spin text-green-500 mb-4" />
        <p className="text-gray-400">Loading dashboard...</p>
        <p className="text-gray-500 text-sm mt-2">Connecting to backend</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Live Dashboard</h1>
          {lastUpdate && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Updated: {lastUpdate.toLocaleTimeString()}
              {metrics?.current_sensor_data && ` | Temp: ${metrics.current_sensor_data.temperature}°C`}
            </p>
          )}
        </div>
        <div className="flex space-x-2">
          <button onClick={() => setDebug(!debug)} className="btn-secondary text-sm">
            {debug ? 'Hide Debug' : 'Debug'}
          </button>
          <button onClick={fetchMetrics} className="btn-secondary text-sm">
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/50 border border-red-300 dark:border-red-700 rounded-lg text-red-700 dark:text-red-200">
          Error: {error}
        </div>
      )}

      {/* Debug Panel */}
      {debug && (
        <div className="mb-6 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg font-mono text-sm text-gray-700 dark:text-gray-300 overflow-x-auto">
          <h3 className="text-gray-900 dark:text-white font-bold mb-2">RAW API RESPONSE:</h3>
          <pre className="whitespace-pre-wrap">{JSON.stringify(metrics, null, 2)}</pre>
        </div>
      )}

      {metrics?.current_sensor_data ? (
        <>
          <div className="mb-6">
            <QuickActions sensorData={metrics.current_sensor_data} onIrrigate={() => alert('Demo')} />
          </div>
          <div className="grid lg:grid-cols-2 gap-6 mb-6">
            <SensorGrid sensorData={metrics.current_sensor_data} />
            <WeatherWidget weather={metrics.weather} />
          </div>
          <div className="grid lg:grid-cols-2 gap-6">
            <ResourceMetrics resourceSummary={metrics.resource_summary} />
            <AlertList alerts={metrics.recent_alerts} />
          </div>
        </>
      ) : (
        <div className="card text-center py-12">
          <p className="text-gray-400 text-lg mb-2">No sensor data received yet</p>
          <p className="text-gray-500 mb-4">Check if Arduino USB bridge is running</p>
          <div className="space-x-4">
            <button onClick={() => window.open('http://localhost:8000/docs', '_blank')} className="btn-primary">
              View API Docs
            </button>
            <button onClick={fetchMetrics} className="btn-secondary">
              Retry
            </button>
          </div>
          <div className="mt-8 text-sm text-gray-600 dark:text-gray-400">
            <p>Make sure:</p>
            <ul className="mt-2 space-y-1">
              <li>✓ Backend server is running on port 8000</li>
              <li>✓ USB bridge is connected to Arduino on COM6</li>
              <li>✓ You are logged in with valid authentication</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
