import React, { useState } from 'react';
import { useAPI } from '../hooks/useAPI';

interface DashboardProps {
  userId?: string;
  className?: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ userId, className }) => {
  const [expanded, setExpanded] = useState(false);
  const { data, loading, error } = useAPI(userId ? `/api/users/${userId}` : '/api/userprofile');
  
  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">Error: {error.message}</div>;
  
  return (
    <div className={`dashboard ${className || ''}`}>
      <div className="component-header" onClick={() => setExpanded(!expanded)}>
        <h3>Dashboard {expanded ? '▼' : '▶'}</h3>
      </div>
      
      {expanded && (
        <div className="component-content">
          {data?.name && <p><strong>Name:</strong> {data.name}</p>}
          {data?.email && <p><strong>Email:</strong> {data.email}</p>}
          {data?.status && <p><strong>Status:</strong> {data.status}</p>}
          
          <details style={{ marginTop: '1rem' }}>
            <summary>Raw Data (Dev)</summary>
            <pre style={{ background: '#f5f5f5', padding: '1rem', overflow: 'auto' }}>
              {JSON.stringify(data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
};
