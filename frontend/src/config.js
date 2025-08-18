// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// Helper function to make API calls
export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`
  const token = localStorage.getItem('authToken')
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers
    }
  }
  
  const response = await fetch(url, { ...defaultOptions, ...options })
  
  if (response.status === 403) {
    const data = await response.json()
    if (data.trial_expired) {
      // Handle trial expiration
      throw new Error('TRIAL_EXPIRED')
    }
  }
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return response.json()
}

