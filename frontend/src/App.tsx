import React, { useEffect, useState } from 'react';
import { apiClient } from './services/apiClient';

function App() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    apiClient.get('/api/status').then(res => setData(res.data));
  }, []);
  
  return (
    <div className="App">
      <h1>Dual-Agent Project</h1>
      <p>Status: {data?.status || 'Loading...'}</p>
    </div>
  );
}
export default App;