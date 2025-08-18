import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import Dashboard from '@/components/Dashboard'
import Contacts from '@/components/Contacts'
import Pipelines from '@/components/Pipelines'
import Campaigns from '@/components/Campaigns'
import Automation from '@/components/Automation'
import Analytics from '@/components/Analytics'
import WorkflowBuilder from '@/components/WorkflowBuilder'
import FunnelBuilder from '@/components/FunnelBuilder'
import Communications from '@/components/Communications'
import AIInsights from '@/components/AIInsights'
import Login from '@/components/Login'
import PricingPage from '@/components/PricingPage'
import WebsiteBuilder from '@/components/WebsiteBuilder'
import WhiteLabelProgram from '@/components/WhiteLabelProgram'
import DomainManager from '@/components/DomainManager'
import SubscriptionUpgrade from '@/components/SubscriptionUpgrade'
import TrialBanner from '@/components/TrialBanner'
import { apiCall } from './config'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showUpgrade, setShowUpgrade] = useState(false)

  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('authToken')
      const storedUser = localStorage.getItem('user')
      
      if (token && storedUser) {
        const userData = JSON.parse(storedUser)
        
        // Verify token is still valid and get updated user info
        try {
          const response = await apiCall('/api/subscription/status')
          setUser(response)
        } catch (error) {
          if (error.message === 'TRIAL_EXPIRED') {
            setUser(userData)
            setShowUpgrade(true)
          } else {
            // Token invalid, clear auth
            handleLogout()
          }
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      handleLogout()
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = async (userData, token) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('authToken', token)
    localStorage.setItem('isAuthenticated', 'true')
    
    // Check if trial is expired
    if (userData.is_trial_expired) {
      setShowUpgrade(true)
    }
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('user')
    localStorage.removeItem('authToken')
    localStorage.removeItem('isAuthenticated')
    setShowUpgrade(false)
  }

  const handleTrialExpired = () => {
    setShowUpgrade(true)
  }

  const handleUpgradeSuccess = (updatedUser, subscription) => {
    setUser(updatedUser)
    localStorage.setItem('user', JSON.stringify(updatedUser))
    setShowUpgrade(false)
  }

  const handleShowUpgrade = () => {
    setShowUpgrade(true)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user) {
    return (
      <Router>
        <Routes>
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="*" element={<Login onLogin={handleLogin} />} />
        </Routes>
      </Router>
    )
  }

  // If trial expired and not showing upgrade modal, force upgrade
  if (user.is_trial_expired && !showUpgrade) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <SubscriptionUpgrade 
          user={user}
          onUpgrade={handleUpgradeSuccess}
          onClose={() => {}} // Can't close if trial expired
        />
      </div>
    )
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Layout user={user} onLogout={handleLogout}>
          {/* Trial Banner */}
          <TrialBanner 
            user={user}
            onUpgrade={handleShowUpgrade}
            onDismiss={() => {}}
          />
          
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/contacts" element={<Contacts user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/pipelines" element={<Pipelines user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/campaigns" element={<Campaigns user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/automation" element={<Automation user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/automation/workflows" element={<WorkflowBuilder user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/analytics" element={<Analytics user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/communications" element={<Communications user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/funnels" element={<FunnelBuilder user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/websites" element={<WebsiteBuilder user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/white-label" element={<WhiteLabelProgram user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/domains" element={<DomainManager user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/ai-insights" element={<AIInsights user={user} onTrialExpired={handleTrialExpired} />} />
            <Route path="/pricing" element={<PricingPage />} />
          </Routes>

          {/* Upgrade Modal */}
          {showUpgrade && (
            <SubscriptionUpgrade 
              user={user}
              onUpgrade={handleUpgradeSuccess}
              onClose={() => !user.is_trial_expired && setShowUpgrade(false)}
            />
          )}
        </Layout>
      </div>
    </Router>
  )
}

export default App

