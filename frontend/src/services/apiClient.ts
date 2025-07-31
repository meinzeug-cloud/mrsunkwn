import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auto-retry logic
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 503) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      return apiClient.request(error.config);
    }
    return Promise.reject(error);
  }
);