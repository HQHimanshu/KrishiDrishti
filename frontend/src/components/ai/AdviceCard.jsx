import React from 'react'
import { AlertTriangle, CheckCircle, Info, Lightbulb, Droplets, Clock, Zap, Cloud, Thermometer } from 'lucide-react'
import { RECOMMENDATION_TYPES } from '../../utils/constants'

const AdviceCard = ({ advice }) => {
  const getRecommendationIcon = (type) => {
    const rec = RECOMMENDATION_TYPES[type]
    const Icon = {
      IRRIGATE: Droplets,
      WAIT: Clock,
      FERTILIZE: Lightbulb
    }[type] || Info

    const color = {
      IRRIGATE: 'text-blue-400',
      WAIT: 'text-yellow-400',
      FERTILIZE: 'text-green-400'
    }[type] || 'text-gray-400'

    return <Icon className={color} size={24} />
  }

  const getAlertClass = (risk) => {
    if (!risk) return 'hidden'
    return 'bg-red-100 dark:bg-red-900/50 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-200'
  }

  return (
    <div className="space-y-4 animate-fadeIn">
      {/* Recommendation Header */}
      <div className="bg-gradient-to-r from-primary-100 to-purple-100 dark:from-primary-900/50 dark:to-purple-900/50 rounded-lg p-4 border border-primary-300 dark:border-primary-700">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            {getRecommendationIcon(advice.recommendation)}
          </div>
          <div className="flex-1">
            <h4 className="text-gray-900 dark:text-white font-bold text-lg mb-1">
              {advice.recommendation?.replace('_', ' ')}
            </h4>
            {advice.confidence_score && (
              <div className="text-gray-600 dark:text-gray-400 text-sm">
                Confidence: {advice.confidence_score}%
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Reason */}
      <div className="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
        <h5 className="text-blue-700 dark:text-blue-300 font-semibold mb-2 flex items-center space-x-2">
          <Info size={16} />
          <span>Reason</span>
        </h5>
        <p className="text-gray-700 dark:text-gray-300 text-sm">{advice.reason}</p>
      </div>

      {/* Action Steps */}
      <div className="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
        <h5 className="text-green-700 dark:text-green-300 font-semibold mb-2 flex items-center space-x-2">
          <CheckCircle size={16} />
          <span>Action Steps</span>
        </h5>
        <p className="text-gray-700 dark:text-gray-300 text-sm whitespace-pre-line">{advice.action}</p>
      </div>

      {/* Optimization Tips */}
      {advice.optimization_tips && (
        <div className="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">
          <h5 className="text-purple-700 dark:text-purple-300 font-semibold mb-2 flex items-center space-x-2">
            <Zap size={16} />
            <span>Optimization Techniques</span>
          </h5>
          <p className="text-gray-700 dark:text-gray-300 text-sm whitespace-pre-line">{advice.optimization_tips}</p>
        </div>
      )}

      {/* Estimated Impact */}
      {advice.estimated_impact && (
        <div className="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4">
          <h5 className="text-amber-700 dark:text-amber-300 font-semibold mb-2 flex items-center space-x-2">
            <Lightbulb size={16} />
            <span>Estimated Impact</span>
          </h5>
          <p className="text-gray-700 dark:text-gray-300 text-sm">{advice.estimated_impact}</p>
        </div>
      )}

      {/* Sensor & Weather Context */}
      {(advice.sensor_context || advice.weather_context) && (
        <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4">
          <h5 className="text-gray-700 dark:text-gray-300 font-semibold mb-3 flex items-center space-x-2">
            <Thermometer size={16} />
            <span>Context Used</span>
          </h5>
          
          {advice.sensor_context && (
            <div className="mb-3">
              <p className="text-xs text-gray-600 dark:text-gray-400 font-semibold mb-1">Sensor Data:</p>
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-700 dark:text-gray-300">
                {advice.sensor_context.temperature && (
                  <div>🌡️ Temp: {advice.sensor_context.temperature}°C</div>
                )}
                {advice.sensor_context.humidity && (
                  <div>💧 Humidity: {advice.sensor_context.humidity}%</div>
                )}
                {advice.sensor_context.soil_moisture_root && (
                  <div>🌱 Soil: {advice.sensor_context.soil_moisture_root} ADC</div>
                )}
                {advice.sensor_context.ph_level && (
                  <div>⚗️ pH: {advice.sensor_context.ph_level}</div>
                )}
              </div>
            </div>
          )}
          
          {advice.weather_context && (
            <div>
              <p className="text-xs text-gray-600 dark:text-gray-400 font-semibold mb-1">Weather:</p>
              <div className="text-xs text-gray-700 dark:text-gray-300 flex items-center space-x-2">
                <Cloud size={14} />
                <span>{advice.weather_context.description}, {advice.weather_context.temperature}°C</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Risk Warning */}
      {advice.risk && (
        <div className={`rounded-lg p-4 border ${getAlertClass(advice.risk)}`}>
          <h5 className="font-semibold mb-2 flex items-center space-x-2">
            <AlertTriangle size={16} />
            <span>Warning</span>
          </h5>
          <p className="text-sm">{advice.risk}</p>
        </div>
      )}

      {/* Language */}
      {advice.language && (
        <div className="text-gray-500 dark:text-gray-400 text-xs text-right">
          Language: {advice.language.toUpperCase()}
        </div>
      )}
    </div>
  )
}

export default AdviceCard
