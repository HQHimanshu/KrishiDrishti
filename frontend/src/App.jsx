import React, { useState, useEffect, createContext, useContext } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
import Advice from './pages/Advice'
import Resources from './pages/Resources'
import Notifications from './pages/Notifications'
import Profile from './pages/Profile'
import PhoneLogin from './components/auth/PhoneLogin'
import Navbar from './components/common/Navbar'
import Footer from './components/common/Footer'
import OfflineBanner from './components/common/OfflineBanner'
import { useTranslation } from 'react-i18next'

// Auth Context
const AuthContext = createContext(null)

export const useAuth = () => useContext(AuthContext)

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const { i18n } = useTranslation()

  useEffect(() => {
    // Check for stored token
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (token && userData) {
      setUser(JSON.parse(userData))
      // Set user's preferred language
      const parsedUser = JSON.parse(userData)
      if (parsedUser.language) {
        i18n.changeLanguage(parsedUser.language)
      }
    }
    setLoading(false)
  }, [i18n])

  const login = (userData, token) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(userData))
    setUser(userData)
    i18n.changeLanguage(userData.language || 'en')
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  const updateUser = (updatedData) => {
    const updatedUser = { ...user, ...updatedData }
    localStorage.setItem('user', JSON.stringify(updatedUser))
    setUser(updatedUser)
    if (updatedData.language) {
      i18n.changeLanguage(updatedData.language)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="text-6xl mb-4">🌾</div>
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-500 mx-auto"></div>
          <p className="mt-4 text-gray-400 text-lg font-medium">Loading KrishiDrishti...</p>
        </div>
      </div>
    )
  }

  return (
    <ThemeProvider>
      <AuthContext.Provider value={{ user, login, logout, updateUser }}>
        <Router>
          <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 flex flex-col transition-colors duration-300">
            <Navbar />
            <main className="flex-grow pb-20">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={!user ? <PhoneLogin /> : <Navigate to="/dashboard" />} />
                <Route
                  path="/dashboard"
                  element={user ? <Dashboard /> : <Navigate to="/login" />}
                />
                <Route
                  path="/analytics"
                  element={user ? <Analytics /> : <Navigate to="/login" />}
                />
                <Route
                  path="/advice"
                  element={user ? <Advice /> : <Navigate to="/login" />}
                />
                <Route
                  path="/resources"
                  element={user ? <Resources /> : <Navigate to="/login" />}
                />
                <Route
                  path="/notifications"
                  element={user ? <Notifications /> : <Navigate to="/login" />}
                />
                <Route
                  path="/profile"
                  element={user ? <Profile /> : <Navigate to="/login" />}
                />
              </Routes>
            </main>
            <Footer />
            <OfflineBanner />
          </div>
        </Router>
      </AuthContext.Provider>
    </ThemeProvider>
  )
}

export default App
