
import React from 'react';
import { useAPI } from '../hooks/useAPI';

interface UserProfileProps {
  // TODO: Define props
}

export const UserProfile: React.FC<UserProfileProps> = (props) => {
  const { data, loading, error } = useAPI('/api/userprofile');
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div className="userprofile">
      {/* TODO: Implement component */}
      <h2>UserProfile</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};
