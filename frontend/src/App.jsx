import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './components/Login';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import Contacts from './components/Contacts';
import Settings from './components/Settings';
import SubscriptionPlans from './components/SubscriptionPlans';
import './App.css';

// Simple components for other routes
const Pipeline = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Sales Pipeline</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">Pipeline management coming soon...</p>
    </div>
  </div>
);

const Messages = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Messages</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">Unified inbox coming soon...</p>
    </div>
  </div>
);

const Analytics = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">Advanced analytics coming soon...</p>
    </div>
  </div>
);

// Comprehensive business platform components coming soon
const Websites = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Website Builder</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">AI-powered website builder coming soon...</p>
    </div>
  </div>
);

const Content = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Content Creation</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">AI content generation and publishing coming soon...</p>
    </div>
  </div>
);

const Funnels = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Marketing Funnels</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">AI-generated marketing funnels coming soon...</p>
    </div>
  </div>
);

const Ecommerce = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">E-commerce</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">Online store and product management coming soon...</p>
    </div>
  </div>
);

const SubAccounts = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const hasWhiteLabelAccess = user.role === 'master' || user.subscription_tier === 'white_label';
  
  if (!hasWhiteLabelAccess) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">Sub-Accounts</h1>
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <div className="text-yellow-600 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold mb-2">White Label Features Required</h3>
          <p className="text-gray-600 mb-4">Sub-account management is available with White Label tier subscription.</p>
          <button className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors">
            Upgrade to White Label
          </button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Sub-Accounts Management</h1>
      <div className="bg-white p-8 rounded-lg shadow text-center">
        <p className="text-gray-600">White-label sub-account management coming soon...</p>
        <p className="text-sm text-green-600 mt-2">✅ White Label access verified</p>
      </div>
    </div>
  );
};

const WhiteLabel = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const hasWhiteLabelAccess = user.role === 'master' || user.subscription_tier === 'white_label';
  
  if (!hasWhiteLabelAccess) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">White Label Settings</h1>
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <div className="text-yellow-600 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold mb-2">White Label Features Required</h3>
          <p className="text-gray-600 mb-4">White label branding and settings are available with White Label tier subscription.</p>
          <button className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors">
            Upgrade to White Label
          </button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">White Label Settings</h1>
      <div className="bg-white p-8 rounded-lg shadow text-center">
        <p className="text-gray-600">White-label branding customization coming soon...</p>
        <p className="text-sm text-green-600 mt-2">✅ White Label access verified</p>
      </div>
    </div>
  );
};

const Automation = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Automation</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">Marketing automation and workflows coming soon...</p>
    </div>
  </div>
);

// Protected Route component
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/" replace />;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Brainstorm AI Kit...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route 
          path="/" 
          element={
            isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />
          } 
        />
        
        {/* Protected routes */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="contacts" element={<Contacts />} />
          <Route path="websites" element={<Websites />} />
          <Route path="content" element={<Content />} />
          <Route path="funnels" element={<Funnels />} />
          <Route path="ecommerce" element={<Ecommerce />} />
          <Route path="sub-accounts" element={<SubAccounts />} />
          <Route path="white-label" element={<WhiteLabel />} />
          <Route path="automation" element={<Automation />} />
          <Route path="pipeline" element={<Pipeline />} />
          <Route path="messages" element={<Messages />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="plans" element={<SubscriptionPlans />} />
          <Route path="settings" element={<Settings />} />
        </Route>

        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
