import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../App'
import { useTranslation } from 'react-i18next'
import ThemeSwitcher from './ThemeSwitcher'
import {
  Home,
  LayoutDashboard,
  BarChart3,
  MessageSquare,
  Droplets,
  Bell,
  User,
  Menu,
  X
} from 'lucide-react'

const Navbar = () => {
  const { user, logout } = useAuth()
  const { t } = useTranslation()
  const location = useLocation()
  const [isOpen, setIsOpen] = React.useState(false)

  const navItems = [
    { path: '/', icon: Home, label: t('nav.home') },
    { path: '/dashboard', icon: LayoutDashboard, label: t('nav.dashboard') },
    { path: '/analytics', icon: BarChart3, label: t('nav.analytics') },
    { path: '/advice', icon: MessageSquare, label: t('nav.advice') },
    { path: '/resources', icon: Droplets, label: t('nav.resources') },
    { path: '/notifications', icon: Bell, label: t('nav.notifications') },
    { path: '/profile', icon: User, label: t('nav.profile') }
  ]

  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <span className="text-2xl">🌾</span>
              <span className="text-xl font-bold text-primary-500">KrishiDrishti</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                    isActive(item.path)
                      ? 'bg-primary-500 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </Link>
              )
            })}

            <ThemeSwitcher />

            {user ? (
              <button
                onClick={logout}
                className="ml-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              >
                {t('nav.logout')}
              </button>
            ) : (
              <Link
                to="/login"
                className="ml-4 px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors"
              >
                {t('nav.login')}
              </Link>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-300 hover:text-white p-2"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden bg-gray-900 border-t border-gray-700 animate-fadeIn">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsOpen(false)}
                  className={`flex items-center space-x-3 px-3 py-3 rounded-lg transition-colors ${
                    isActive(item.path)
                      ? 'bg-primary-500 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              )
            })}
            
            {user ? (
              <button
                onClick={() => {
                  logout()
                  setIsOpen(false)
                }}
                className="w-full text-left px-3 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              >
                {t('nav.logout')}
              </button>
            ) : (
              <Link
                to="/login"
                onClick={() => setIsOpen(false)}
                className="flex items-center space-x-3 px-3 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors"
              >
                <User size={20} />
                <span>{t('nav.login')}</span>
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}

export default Navbar
