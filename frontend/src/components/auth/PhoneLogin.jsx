import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../App'
import { useTranslation } from 'react-i18next'
import { authAPI } from '../../services/api'
import { validatePhone, validateOTP } from '../../utils/validators'
import { Phone, Key, Send, CheckCircle } from 'lucide-react'

const PhoneLogin = () => {
  const { login } = useAuth()
  const { t } = useTranslation()
  const navigate = useNavigate()

  const [phone, setPhone] = useState('')
  const [otp, setOtp] = useState('')
  const [step, setStep] = useState(1) // 1: Phone, 2: OTP
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [mockOTP, setMockOTP] = useState(null)

  const handleSendOTP = async (e) => {
    e.preventDefault()
    setError('')

    if (!validatePhone(phone)) {
      setError('Please enter a valid phone number')
      return
    }

    setLoading(true)
    try {
      const response = await authAPI.sendOTP(phone)
      setMockOTP(response.data.mock_otp)
      setStep(2)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send OTP')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOTP = async (e) => {
    e.preventDefault()
    setError('')

    if (!validateOTP(otp)) {
      setError('Please enter a valid 6-digit OTP')
      return
    }

    setLoading(true)
    try {
      const response = await authAPI.verifyOTP(phone, otp)
      const { access_token, user: userData } = response.data
      login(userData, access_token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid OTP')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🌾</div>
          <h1 className="text-3xl font-bold text-primary-500">KrishiDrishti</h1>
          <p className="text-gray-400 mt-2">AI-Powered Smart Farming Assistant</p>
        </div>

        {/* Login Card */}
        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-white mb-6">
            {step === 1 ? 'Login with Phone' : 'Verify OTP'}
          </h2>

          {error && (
            <div className="mb-4 p-3 bg-red-900 border border-red-700 rounded-lg text-red-200">
              {error}
            </div>
          )}

          {mockOTP && (
            <div className="mb-4 p-3 bg-blue-900 border border-blue-700 rounded-lg text-blue-200">
              <strong>Demo OTP:</strong> {mockOTP}
            </div>
          )}

          <form onSubmit={step === 1 ? handleSendOTP : handleVerifyOTP}>
            {step === 1 ? (
              <div>
                <label className="block text-gray-300 mb-2">Phone Number</label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="+91 98765 43210"
                    className="input-field pl-10"
                    autoFocus
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary w-full mt-4 flex items-center justify-center space-x-2 disabled:opacity-50"
                >
                  <Send size={18} />
                  <span>{loading ? 'Sending...' : 'Send OTP'}</span>
                </button>
              </div>
            ) : (
              <div>
                <label className="block text-gray-300 mb-2">Enter OTP</label>
                <div className="relative">
                  <Key className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    placeholder="123456"
                    maxLength="6"
                    className="input-field pl-10 text-center text-2xl tracking-widest"
                    autoFocus
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary w-full mt-4 flex items-center justify-center space-x-2 disabled:opacity-50"
                >
                  <CheckCircle size={18} />
                  <span>{loading ? 'Verifying...' : 'Verify OTP'}</span>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setStep(1)
                    setOtp('')
                    setError('')
                  }}
                  className="btn-secondary w-full mt-2"
                >
                  Change Number
                </button>
              </div>
            )}
          </form>
        </div>

        {/* Info */}
        <div className="mt-6 text-center text-gray-400 text-sm">
          <p>Supports Hindi, Marathi & English</p>
          <p className="mt-1">Works offline in rural areas 🌾</p>
        </div>
      </div>
    </div>
  )
}

export default PhoneLogin
