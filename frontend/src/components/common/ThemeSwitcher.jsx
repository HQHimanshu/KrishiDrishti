import React from 'react'
import { useTheme } from '../../context/ThemeContext'
import { Sun, Moon } from 'lucide-react'

const ThemeSwitcher = () => {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-600 transition-colors"
      title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
    >
      {theme === 'dark' ? (
        <Sun size={20} className="text-yellow-400" />
      ) : (
        <Moon size={20} className="text-gray-600" />
      )}
    </button>
  )
}

export default ThemeSwitcher
