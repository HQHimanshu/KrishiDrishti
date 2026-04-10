import React from 'react'
import { Cloud, Wind, Droplets, Gauge, AlertTriangle, Sun } from 'lucide-react'
import { formatTemperature, formatHumidity } from '../../utils/formatters'

const WeatherWidget = ({ weather }) => {
  if (!weather) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Weather</h3>
        <div className="text-gray-600 dark:text-gray-400 text-center py-8">
          <Cloud size={48} className="mx-auto mb-4 opacity-50" />
          <p>Weather data loading...</p>
          <p className="text-sm mt-2">Fetching live Mumbai weather</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
        <Sun size={20} className="text-yellow-500" />
        <span>Weather (Mumbai)</span>
      </h3>

      <div className="space-y-4">
        {/* Current Weather */}
        <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/50 dark:to-purple-900/50 rounded-lg p-6 border border-blue-200 dark:border-blue-700">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
                {formatTemperature(weather.temperature)}
              </div>
              <div className="text-gray-700 dark:text-gray-300 capitalize font-medium">
                {weather.description}
              </div>
              <div className="text-gray-600 dark:text-gray-400 text-sm mt-1">
                Feels like {formatTemperature(weather.feels_like)}
              </div>
            </div>
            <Cloud className="text-blue-500 dark:text-blue-400" size={64} />
          </div>
        </div>

        {/* Details */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-center space-x-3 border border-gray-200 dark:border-gray-600">
            <Droplets className="text-blue-500 dark:text-blue-400" size={20} />
            <div>
              <div className="text-gray-600 dark:text-gray-400 text-xs">Humidity</div>
              <div className="text-gray-900 dark:text-white font-semibold">{formatHumidity(weather.humidity)}</div>
            </div>
          </div>

          <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-center space-x-3 border border-gray-200 dark:border-gray-600">
            <Wind className="text-cyan-500 dark:text-cyan-400" size={20} />
            <div>
              <div className="text-gray-600 dark:text-gray-400 text-xs">Wind Speed</div>
              <div className="text-gray-900 dark:text-white font-semibold">{weather.wind_speed} m/s</div>
            </div>
          </div>

          <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 flex items-center space-x-3 border border-gray-200 dark:border-gray-600">
            <Gauge className="text-purple-500 dark:text-purple-400" size={20} />
            <div>
              <div className="text-gray-600 dark:text-gray-400 text-xs">Pressure</div>
              <div className="text-gray-900 dark:text-white font-semibold">{weather.pressure} hPa</div>
            </div>
          </div>
        </div>

        {/* Alert */}
        {weather.alert && (
          <div className="bg-yellow-50 dark:bg-yellow-900/50 border border-yellow-300 dark:border-yellow-700 rounded-lg p-3 flex items-start space-x-3">
            <AlertTriangle className="text-yellow-500 dark:text-yellow-400 flex-shrink-0 mt-1" size={20} />
            <div className="text-yellow-700 dark:text-yellow-200 text-sm">{weather.alert}</div>
          </div>
        )}

        {/* Live Data Badge */}
        <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
          <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
          Live data from OpenWeatherMap API
        </div>
      </div>
    </div>
  )
}

export default WeatherWidget
