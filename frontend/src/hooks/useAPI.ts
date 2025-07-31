import { useState, useEffect } from 'react';
import { apiClient } from '../services/apiClient';

interface UseAPIResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useAPI<T = any>(endpoint: string): UseAPIResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiClient.get(endpoint);
        setData(response.data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  return { data, loading, error };
}