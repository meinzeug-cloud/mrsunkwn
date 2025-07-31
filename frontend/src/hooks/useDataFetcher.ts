import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../services/apiClient';

interface useDataFetcherOptions {
  endpoint: string;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

interface useDataFetcherResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
  lastFetched: Date | null;
}

export function useDataFetcher<T = any>(
  options: useDataFetcherOptions
): useDataFetcherResult<T> {
  const { endpoint, autoRefresh = false, refreshInterval = 30000 } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [lastFetched, setLastFetched] = useState<Date | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get(endpoint);
      setData(response.data);
      setLastFetched(new Date());
      console.log(`✅ useDataFetcher fetched data from ${endpoint}`);
    } catch (err) {
      setError(err as Error);
      console.error(`❌ useDataFetcher error:`, err);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(fetchData, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshInterval, fetchData]);

  return { data, loading, error, refetch: fetchData, lastFetched };
}
