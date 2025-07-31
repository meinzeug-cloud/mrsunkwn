import React from 'react';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  message?: string;
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  size = 'medium', 
  message = 'Loading...', 
  className 
}) => {
  const getSpinnerSize = () => {
    switch (size) {
      case 'small': return '16px';
      case 'large': return '48px';
      default: return '32px';
    }
  };

  return (
    <div className={`loading-spinner ${className || ''}`}>
      <div className="spinner-container">
        <div 
          style={{
            width: getSpinnerSize(),
            height: getSpinnerSize(),
            border: '2px solid #f3f3f3',
            borderTop: '2px solid #3498db',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            display: 'inline-block'
          }}
        />
        {message && <p className="spinner-message">{message}</p>}
      </div>
    </div>
  );
};
