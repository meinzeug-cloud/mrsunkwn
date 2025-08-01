import React, { useEffect, useState } from 'react';
import { apiClient } from './services/apiClient';
import { UserProfile } from './components/UserProfile';
import { Dashboard } from './pages/Dashboard';
import { LoadingSpinner } from './components/LoadingSpinner';

function App() {
  const [data, setData] = useState(null);
  const [currentView, setCurrentView] = useState<'home' | 'dashboard'>('home');
  
  useEffect(() => {
    apiClient.get('/api/status').then(res => setData(res.data));
  }, []);
  
  return (
    <div className="App">
      <header style={{ marginBottom: '2rem' }}>
        <h1>🎨 Frontend Sprint Demo</h1>
        <p>Status: {data?.status || 'Loading...'}</p>
        
        <nav style={{ marginTop: '1rem' }}>
          <button 
            onClick={() => setCurrentView('home')}
            style={{ 
              marginRight: '1rem', 
              padding: '0.5rem 1rem',
              backgroundColor: currentView === 'home' ? '#3498db' : '#ecf0f1',
              color: currentView === 'home' ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            🏠 Home
          </button>
          <button 
            onClick={() => setCurrentView('dashboard')}
            style={{ 
              padding: '0.5rem 1rem',
              backgroundColor: currentView === 'dashboard' ? '#3498db' : '#ecf0f1',
              color: currentView === 'dashboard' ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            📊 Dashboard
          </button>
        </nav>
      </header>
      
      <main>
        {currentView === 'home' ? (
          <div>
            <div style={{ marginBottom: '2rem', padding: '1rem', background: '#e8f6f3', borderRadius: '8px' }}>
              <h2>✅ Frontend Sprint Complete!</h2>
              <p>The following components were generated by <code>./scripts/start_frontend_agent.sh</code>:</p>
              <ul>
                <li>🧩 <strong>UserProfile</strong> - Interactive user component with collapsible UI</li>
                <li>⏳ <strong>LoadingSpinner</strong> - Reusable loading indicator</li>
                <li>📄 <strong>Dashboard</strong> - Complete page layout</li>
                <li>🎣 <strong>useDataFetcher</strong> - Custom hook for API data fetching</li>
              </ul>
            </div>
            
            <div style={{ marginTop: '2rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
              <h3>🧩 Generated Component Demo:</h3>
              <UserProfile />
            </div>
            
            <div style={{ marginTop: '2rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
              <h3>⏳ Loading Component Demo:</h3>
              <LoadingSpinner message="Frontend Sprint in action..." />
            </div>
          </div>
        ) : (
          <Dashboard />
        )}
      </main>
    </div>
  );
}
export default App;