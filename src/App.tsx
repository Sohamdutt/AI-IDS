import React from 'react';
import NetworkDashboard from './components/NetworkDashboard';
import VulnerabilityScanner from './components/VulnerabilityScanner';
import AuthTabs from './components/AuthTabs';
import { AuthProvider, useAuth } from './context/AuthContext';

function MainContent() {
  const { isAuthenticated, user, logout } = useAuth();
  const [activeTab, setActiveTab] = React.useState<'scanner' | 'network'>('scanner');

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto">
        <AuthTabs />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Security Suite</h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-600">Welcome, {user?.name}</span>
          <button
            onClick={logout}
            className="text-sm bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('scanner')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'scanner'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Vulnerability Scanner
            </button>
            <button
              onClick={() => setActiveTab('network')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'network'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Network Security
            </button>
          </nav>
        </div>
      </div>

      {activeTab === 'scanner' ? <VulnerabilityScanner /> : <NetworkDashboard />}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50 py-12 px-4">
        <MainContent />
      </div>
    </AuthProvider>
  );
}

export default App;