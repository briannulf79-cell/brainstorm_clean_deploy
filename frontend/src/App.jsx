import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './components/Login';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import Contacts from './components/Contacts';
import Settings from './components/Settings';
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

const SubAccounts = () => (
  <div className="space-y-6">
    <h1 className="text-3xl font-bold text-gray-900">Sub-Accounts</h1>
    <div className="bg-white p-8 rounded-lg shadow text-center">
      <p className="text-gray-600">White-label client management coming soon...</p>
    </div>
  </div>
);

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
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
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
          <Route path="automation" element={<Automation />} />
          <Route path="pipeline" element={<Pipeline />} />
          <Route path="messages" element={<Messages />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="settings" element={<Settings />} />
        </Route>

        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
