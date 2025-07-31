import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useAPI } from '../hooks/useAPI';
import { useAuth } from '../hooks/useAuth';
import { useLocalStorage } from '../hooks/useLocalStorage';

// Interfaces and Types
interface LessonViewerProps {
  userId?: string;
  className?: string;
  theme?: 'light' | 'dark' | 'auto';
  size?: 'small' | 'medium' | 'large';
  variant?: 'default' | 'compact' | 'detailed';
  enableSearch?: boolean;
  enableFilters?: boolean;
  enableSorting?: boolean;
  enablePagination?: boolean;
  enableExport?: boolean;
  enableRefresh?: boolean;
  autoRefresh?: boolean;
  refreshInterval?: number;
  onItemClick?: (item: any) => void;
  onItemSelect?: (items: any[]) => void;
  onError?: (error: Error) => void;
  onSuccess?: (data: any) => void;
  customActions?: Array<{
    label: string;
    icon?: string;
    onClick: (item: any) => void;
    disabled?: (item: any) => boolean;
  }>;
}

interface LessonViewerState {
  expanded: boolean;
  selectedItems: Set<string>;
  searchQuery: string;
  filters: Record<string, any>;
  sortBy: string;
  sortDirection: 'asc' | 'desc';
  currentPage: number;
  itemsPerPage: number;
  viewMode: 'list' | 'grid' | 'table';
  showModal: boolean;
  modalContent: React.ReactNode;
  lastRefreshed: Date;
}

// Main Component
export const LessonViewer: React.FC<LessonViewerProps> = ({
  userId,
  className = '',
  theme = 'auto',
  size = 'medium',
  variant = 'default',
  enableSearch = true,
  enableFilters = true,
  enableSorting = true,
  enablePagination = true,
  enableExport = false,
  enableRefresh = true,
  autoRefresh = false,
  refreshInterval = 30000,
  onItemClick,
  onItemSelect,
  onError,
  onSuccess,
  customActions = []
}) => {
  // State Management
  const [state, setState] = useState<LessonViewerState>({
    expanded: true,
    selectedItems: new Set<string>(),
    searchQuery: '',
    filters: {},
    sortBy: 'created_at',
    sortDirection: 'desc',
    currentPage: 1,
    itemsPerPage: 20,
    viewMode: 'list',
    showModal: false,
    modalContent: null,
    lastRefreshed: new Date()
  });

  // Refs
  const searchInputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Custom Hooks
  const [preferences, setPreferences] = useLocalStorage(`lessonviewer_preferences`, {
    viewMode: 'list',
    itemsPerPage: 20,
    sortBy: 'created_at',
    sortDirection: 'desc'
  });

  // API Configuration
  const apiEndpoint = useMemo(() => {
    const baseUrl = userId ? `/api/lessonviewers/user/${userId}` : `/api/lessonviewers`;
    const queryParams = new URLSearchParams();
    
    if (state.searchQuery) queryParams.append('search', state.searchQuery);
    if (state.sortBy) queryParams.append('sort_by', state.sortBy);
    if (state.sortDirection) queryParams.append('sort_order', state.sortDirection);
    queryParams.append('page', state.currentPage.toString());
    queryParams.append('per_page', state.itemsPerPage.toString());
    
    Object.entries(state.filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        queryParams.append(key, value.toString());
      }
    });
    
    return `${baseUrl}?${queryParams.toString()}`;
  }, [userId, state.searchQuery, state.sortBy, state.sortDirection, state.currentPage, state.itemsPerPage, state.filters]);

  // API Hook
  const { data, loading, error, refetch, lastFetched } = useAPI(apiEndpoint, {
    autoRefresh,
    refreshInterval
  });

  // Update state on data changes
  useEffect(() => {
    if (data) {
      setState(prev => ({ ...prev, lastRefreshed: new Date() }));
      onSuccess?.(data);
    }
  }, [data, onSuccess]);

  // Handle errors
  useEffect(() => {
    if (error) {
      console.error(`LessonViewer error:`, error);
      onError?.(error);
    }
  }, [error, onError]);

  // Event Handlers
  const updateState = useCallback((updates: Partial<LessonViewerState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }, []);

  const handleItemClick = useCallback((item: any, event: React.MouseEvent) => {
    if (event.ctrlKey || event.metaKey) {
      const newSelected = new Set(state.selectedItems);
      if (newSelected.has(item.id)) {
        newSelected.delete(item.id);
      } else {
        newSelected.add(item.id);
      }
      updateState({ selectedItems: newSelected });
      const selectedData = Array.from(newSelected).map(id => data?.items?.find((i: any) => i.id === id)).filter(Boolean);
      onItemSelect?.(selectedData);
    } else {
      onItemClick?.(item);
    }
  }, [state.selectedItems, data?.items, onItemClick, onItemSelect, updateState]);

  const handleSearch = useCallback((query: string) => {
    updateState({ 
      searchQuery: query,
      currentPage: 1
    });
  }, [updateState]);

  const handleFilter = useCallback((filterKey: string, value: any) => {
    updateState({ 
      filters: { ...state.filters, [filterKey]: value },
      currentPage: 1
    });
  }, [state.filters, updateState]);

  const handleSort = useCallback((sortBy: string) => {
    const sortDirection = state.sortBy === sortBy && state.sortDirection === 'asc' ? 'desc' : 'asc';
    updateState({ sortBy, sortDirection, currentPage: 1 });
    setPreferences(prev => ({ ...prev, sortBy, sortDirection }));
  }, [state.sortBy, state.sortDirection, updateState, setPreferences]);

  const handlePageChange = useCallback((page: number) => {
    updateState({ currentPage: page });
  }, [updateState]);

  const handleRefresh = useCallback(() => {
    refetch();
    updateState({ lastRefreshed: new Date() });
  }, [refetch, updateState]);

  const handleSelectAll = useCallback(() => {
    if (!data?.items) return;
    
    const allIds = new Set(data.items.map((item: any) => item.id));
    const isAllSelected = data.items.every((item: any) => state.selectedItems.has(item.id));
    
    const newSelected = isAllSelected ? new Set<string>() : allIds;
    updateState({ selectedItems: newSelected });
    const selectedData = Array.from(newSelected).map(id => data.items.find((i: any) => i.id === id)).filter(Boolean);
    onItemSelect?.(selectedData);
  }, [data?.items, state.selectedItems, updateState, onItemSelect]);

  const handleExport = useCallback((format: 'csv' | 'json') => {
    if (!data?.items) return;
    
    const exportData = state.selectedItems.size > 0 
      ? data.items.filter((item: any) => state.selectedItems.has(item.id))
      : data.items;
    
    if (format === 'csv') {
      const csv = convertToCSV(exportData);
      downloadFile(csv, `lessonviewer_export.csv`, 'text/csv');
    } else {
      const json = JSON.stringify(exportData, null, 2);
      downloadFile(json, `lessonviewer_export.json`, 'application/json');
    }
  }, [data?.items, state.selectedItems]);

  // Utility functions
  const convertToCSV = (items: any[]) => {
    if (!items.length) return '';
    const headers = Object.keys(items[0]).join(',');
    const rows = items.map(item => 
      Object.values(item).map(value => 
        typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value
      ).join(',')
    );
    return [headers, ...rows].join('\n');
  };

  const downloadFile = (content: string, filename: string, contentType: string) => {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Render helpers
  const renderToolbar = () => (
    <div className="component-toolbar">
      {enableSearch && (
        <input
          ref={searchInputRef}
          type="text"
          value={state.searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="Search..."
          className="search-input"
        />
      )}
      
      <div className="toolbar-actions">
        {enableRefresh && (
          <button 
            onClick={handleRefresh}
            disabled={loading}
            className="btn btn-secondary"
            title="Refresh"
          >
            🔄 Refresh
          </button>
        )}
        
        {enableExport && data?.items?.length > 0 && (
          <div className="export-buttons">
            <button onClick={() => handleExport('csv')} className="btn btn-secondary">
              📤 CSV
            </button>
            <button onClick={() => handleExport('json')} className="btn btn-secondary">
              📤 JSON
            </button>
          </div>
        )}
        
        <div className="view-mode-selector">
          <button 
            className={`btn ${state.viewMode === 'list' ? 'active' : ''}`}
            onClick={() => updateState({ viewMode: 'list' })}
          >
            📋 List
          </button>
          <button 
            className={`btn ${state.viewMode === 'grid' ? 'active' : ''}`}
            onClick={() => updateState({ viewMode: 'grid' })}
          >
            ⊞ Grid
          </button>
          <button 
            className={`btn ${state.viewMode === 'table' ? 'active' : ''}`}
            onClick={() => updateState({ viewMode: 'table' })}
          >
            📊 Table
          </button>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    if (loading) {
      return (
        <div className="loading-container">
          <div className="loading-spinner">Loading lessonviewers...</div>
        </div>
      );
    }

    if (error) {
      return (
        <div className="error-container">
          <div className="error-message">
            <h4>Error loading lessonviewers</h4>
            <p>{error.message}</p>
            <button onClick={handleRefresh} className="btn btn-primary">
              Try Again
            </button>
          </div>
        </div>
      );
    }

    if (!data?.items || data.items.length === 0) {
      return (
        <div className="empty-state">
          <div className="empty-message">
            <h4>No lessonviewers found</h4>
            <p>{state.searchQuery ? 'Try adjusting your search' : 'Get started by creating your first lessonviewer'}</p>
          </div>
        </div>
      );
    }

    return (
      <div className={`content-container view-mode-${state.viewMode}`}>
        {state.viewMode === 'table' && renderTable()}
        {state.viewMode === 'grid' && renderGrid()}
        {state.viewMode === 'list' && renderList()}
      </div>
    );
  };

  const renderTable = () => (
    <table className="data-table">
      <thead>
        <tr>
          <th>
            <input
              type="checkbox"
              checked={data?.items?.length > 0 && data.items.every((item: any) => state.selectedItems.has(item.id))}
              onChange={handleSelectAll}
            />
          </th>
          <th onClick={() => handleSort('name')}>
            Name 
            {state.sortBy === 'name' && (
              <span className="sort-indicator">
                {state.sortDirection === 'asc' ? '↑' : '↓'}
              </span>
            )}
          </th>
          <th onClick={() => handleSort('status')}>
            Status
            {state.sortBy === 'status' && (
              <span className="sort-indicator">
                {state.sortDirection === 'asc' ? '↑' : '↓'}
              </span>
            )}
          </th>
          <th onClick={() => handleSort('created_at')}>
            Created
            {state.sortBy === 'created_at' && (
              <span className="sort-indicator">
                {state.sortDirection === 'asc' ? '↑' : '↓'}
              </span>
            )}
          </th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {data?.items?.map((item: any) => (
          <tr key={item.id} className={state.selectedItems.has(item.id) ? 'selected' : ''}>
            <td>
              <input
                type="checkbox"
                checked={state.selectedItems.has(item.id)}
                onChange={() => {
                  const newSelected = new Set(state.selectedItems);
                  if (newSelected.has(item.id)) {
                    newSelected.delete(item.id);
                  } else {
                    newSelected.add(item.id);
                  }
                  updateState({ selectedItems: newSelected });
                }}
              />
            </td>
            <td onClick={(e) => handleItemClick(item, e)}>{item.name || 'Untitled'}</td>
            <td>{item.status || 'Unknown'}</td>
            <td>{item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A'}</td>
            <td>
              {customActions.map(action => (
                <button
                  key={action.label}
                  onClick={() => action.onClick(item)}
                  disabled={action.disabled?.(item)}
                  className="btn btn-sm"
                >
                  {action.icon} {action.label}
                </button>
              ))}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );

  const renderGrid = () => (
    <div className="grid-container">
      {data?.items?.map((item: any) => (
        <div 
          key={item.id} 
          className={`grid-item ${state.selectedItems.has(item.id) ? 'selected' : ''}`}
          onClick={(e) => handleItemClick(item, e)}
        >
          <h4>{item.name || 'Untitled'}</h4>
          <p>{item.description || 'No description'}</p>
          <div className="item-meta">
            <span className="status">{item.status || 'Unknown'}</span>
            <span className="date">{item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A'}</span>
          </div>
          <div className="item-actions">
            {customActions.map(action => (
              <button
                key={action.label}
                onClick={(e) => {
                  e.stopPropagation();
                  action.onClick(item);
                }}
                disabled={action.disabled?.(item)}
                className="btn btn-sm"
              >
                {action.icon} {action.label}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  const renderList = () => (
    <div className="list-container">
      {data?.items?.map((item: any) => (
        <div 
          key={item.id} 
          className={`list-item ${state.selectedItems.has(item.id) ? 'selected' : ''}`}
          onClick={(e) => handleItemClick(item, e)}
        >
          <div className="item-content">
            <h4>{item.name || 'Untitled'}</h4>
            <p>{item.description || 'No description'}</p>
            <div className="item-meta">
              <span className="status">Status: {item.status || 'Unknown'}</span>
              <span className="date">Created: {item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A'}</span>
            </div>
          </div>
          <div className="item-actions">
            {customActions.map(action => (
              <button
                key={action.label}
                onClick={(e) => {
                  e.stopPropagation();
                  action.onClick(item);
                }}
                disabled={action.disabled?.(item)}
                className="btn btn-sm"
              >
                {action.icon} {action.label}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  const renderPagination = () => enablePagination && data?.total > state.itemsPerPage && (
    <div className="pagination-container">
      <div className="pagination-info">
        Showing {((state.currentPage - 1) * state.itemsPerPage) + 1} to {Math.min(state.currentPage * state.itemsPerPage, data.total)} of {data.total} items
      </div>
      <div className="pagination-controls">
        <button 
          onClick={() => handlePageChange(state.currentPage - 1)}
          disabled={state.currentPage === 1}
          className="btn btn-secondary"
        >
          Previous
        </button>
        
        <span className="page-info">Page {state.currentPage} of {Math.ceil(data.total / state.itemsPerPage)}</span>
        
        <button 
          onClick={() => handlePageChange(state.currentPage + 1)}
          disabled={state.currentPage >= Math.ceil(data.total / state.itemsPerPage)}
          className="btn btn-secondary"
        >
          Next
        </button>
      </div>
      <div className="items-per-page">
        <select 
          value={state.itemsPerPage}
          onChange={(e) => {
            const newItemsPerPage = Number(e.target.value);
            updateState({ itemsPerPage: newItemsPerPage, currentPage: 1 });
            setPreferences(prev => ({ ...prev, itemsPerPage: newItemsPerPage }));
          }}
        >
          <option value={10}>10 per page</option>
          <option value={20}>20 per page</option>
          <option value={50}>50 per page</option>
          <option value={100}>100 per page</option>
        </select>
      </div>
    </div>
  );

  // Main render
  return (
    <div 
      ref={containerRef}
      className={`lessonviewer-component theme-${theme} size-${size} variant-${variant} ${className}`}
      data-testid="lessonviewer-component"
    >
      <div className="component-header">
        <div className="header-content">
          <h3 className="component-title">
            LessonViewer
            {state.selectedItems.size > 0 && (
              <span className="selection-badge">
                {state.selectedItems.size} selected
              </span>
            )}
          </h3>
          <div className="header-meta">
            {lastFetched && (
              <span className="last-updated">
                Last updated: {lastFetched.toLocaleTimeString()}
              </span>
            )}
            {autoRefresh && (
              <span className="auto-refresh-indicator">
                🔄 Auto-refresh enabled
              </span>
            )}
          </div>
        </div>
        
        <button
          className="expand-toggle"
          onClick={() => updateState({ expanded: !state.expanded })}
          aria-label={state.expanded ? 'Collapse' : 'Expand'}
        >
          {state.expanded ? '▼' : '▶'}
        </button>
      </div>

      {state.expanded && (
        <div className="component-body">
          {renderToolbar()}
          {renderContent()}
          {renderPagination()}
          
          {data?.items && (
            <details className="dev-info" style={{ marginTop: '2rem' }}>
              <summary>Debug Info (Development)</summary>
              <pre style={{ 
                background: '#f5f5f5', 
                padding: '1rem', 
                overflow: 'auto',
                fontSize: '0.8rem'
              }}>
                API Endpoint: {apiEndpoint}{'
'}
                Items Count: {data.items.length}{'
'}
                Total: {data.total}{'
'}
                Selected: {state.selectedItems.size}{'
'}
                Current Page: {state.currentPage}{'
'}
                View Mode: {state.viewMode}{'
'}
                Last Refreshed: {state.lastRefreshed.toISOString()}
              </pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
};

export default LessonViewer;
