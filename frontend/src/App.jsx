import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './components/Dashboard'
import ThreatIntelligence from './components/ThreatIntelligence'
import AssetManagement from './components/AssetManagement'
import LoginPage from './components/LoginPage'
import OAuthCallback from './components/OAuthCallback'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [user, setUser] = useState(null)

  const handleLogin = (userData) => {
    setIsAuthenticated(true)
    setUser(userData)
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    setUser(null)
    localStorage.removeItem('authToken')
  }

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'threat-intel':
        return <ThreatIntelligence />
      case 'assets':
        return <AssetManagement />
      default:
        return <Dashboard />
    }
  }

  if (!isAuthenticated) {
    return (
      <Router>
        <Routes>
          <Route path="/auth/callback" element={<OAuthCallback onLogin={handleLogin} />} />
          <Route path="*" element={<LoginPage onLogin={handleLogin} />} />
        </Routes>
      </Router>
    )
  }

  return (
    <Router>
      <Layout currentPage={currentPage} onPageChange={setCurrentPage} user={user} onLogout={handleLogout}>
        {renderCurrentPage()}
      </Layout>
    </Router>
  )
}

export default App
