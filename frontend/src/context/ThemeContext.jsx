import React, { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext()

export const useTheme = () => useContext(ThemeContext)

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark')
  const [accent, setAccent] = useState(() => localStorage.getItem('accent') || 'green')

  useEffect(() => {
    localStorage.setItem('theme', theme)
    localStorage.setItem('accent', accent)
    
    // Apply theme class to document root
    const root = document.documentElement
    if (theme === 'light') {
      root.classList.remove('dark')
    } else {
      root.classList.add('dark')
    }
  }, [theme, accent])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme, accent, setAccent }}>
      {children}
    </ThemeContext.Provider>
  )
}
