import os
import sys
import time
from datetime import datetime

class SprintRunner:
    def __init__(self, agent_role):
        self.agent = agent_role
        self.sprint_count = 0
        
    def run_sprint(self):
        '''Executes a complete sprint automatically'''
        self.sprint_count += 1
        print(f"\n🏃 Sprint #{self.sprint_count} - {self.agent}")
        
        # 1. Issue Sync
        self._sync_issues()
        
        # 2. Analyze & Prioritize
        tasks = self._prioritize_tasks()
        
        # 3. GENERATE CODE (MOST IMPORTANT PART!)
        for task in tasks:
            if task['type'] in ['feature', 'api', 'component', 'page', 'hook']:
                self._generate_code(task)
            elif task['type'] == 'bug':
                self._fix_code(task)
                
        # 4. Run Tests
        self._run_tests()
        
        # 5. Update Status
        self._update_status()
        
    def _sync_issues(self):
        '''Sync with GitHub issues'''
        print("🔄 Syncing issues...")
        # TODO: Implement issue sync
        
    def _prioritize_tasks(self):
        '''Prioritize and return tasks'''
        print("📋 Prioritizing tasks...")
        # Return more comprehensive tasks for frontend sprint
        if self.agent == 'FRONTEND_AGENT':
            return [
                {'title': 'User Profile Component', 'type': 'component', 'component_name': 'UserProfile'},
                {'title': 'Loading Spinner Component', 'type': 'component', 'component_name': 'LoadingSpinner'},
                {'title': 'Dashboard Page', 'type': 'page', 'page_name': 'Dashboard'},
                {'title': 'Data Fetching Hook', 'type': 'hook', 'hook_name': 'useDataFetcher'}
            ]
        else:
            return [
                {'title': 'Sample Component', 'type': 'component', 'component_name': 'UserProfile'},
                {'title': 'API Endpoint', 'type': 'api', 'endpoint': '/api/users'}
            ]
        
    def _generate_code(self, task):
        '''GENERATES ACTUAL CODE'''
        print(f"💻 Generating code for: {task['title']}")
        
        if self.agent == 'FRONTEND_AGENT':
            if 'component' in task['title'].lower():
                self._create_react_component(task)
            elif 'page' in task['title'].lower():
                self._create_react_page(task)
            elif 'hook' in task['title'].lower():
                self._create_react_hook(task)
            
            # Special handling for specific components
            if task.get('component_name') == 'LoadingSpinner':
                self._create_loading_spinner_component(task)
                
        elif self.agent == 'BACKEND_AGENT':
            if 'endpoint' in task['title'].lower():
                self._create_api_endpoint(task)
            elif 'model' in task['title'].lower():
                self._create_data_model(task)
            elif 'service' in task['title'].lower():
                self._create_service(task)
                
    def _fix_code(self, task):
        '''Fix code for bugs'''
        print(f"🔧 Fixing code for: {task['title']}")
        # TODO: Implement bug fixes
        
    def _run_tests(self):
        '''Run tests'''
        print("🧪 Running tests...")
        # TODO: Implement test execution
        
    def _update_status(self):
        '''Update status'''
        print("📊 Updating status...")
        # TODO: Implement status updates
    
    def _create_react_component(self, task):
        '''Generates React Component'''
        component_name = task.get('component_name', 'NewComponent')
        # Create a more complete and useful component
        code = f'''import React, {{ useState }} from 'react';
import {{ useAPI }} from '../hooks/useAPI';

interface {component_name}Props {{
  userId?: string;
  className?: string;
}}

export const {component_name}: React.FC<{component_name}Props> = ({{ userId, className }}) => {{
  const [expanded, setExpanded] = useState(false);
  const {{ data, loading, error }} = useAPI(userId ? `/api/users/${{userId}}` : '/api/userprofile');
  
  if (loading) return <div className="loading">Loading {component_name.lower()}...</div>;
  if (error) return <div className="error">Error: {{error.message}}</div>;
  
  return (
    <div className={{`{component_name.lower()} ${{className || ''}}`}}>
      <div className="component-header" onClick={{() => setExpanded(!expanded)}}>
        <h3>{component_name} {{expanded ? '▼' : '▶'}}</h3>
      </div>
      
      {{expanded && (
        <div className="component-content">
          {{data?.name && <p><strong>Name:</strong> {{data.name}}</p>}}
          {{data?.email && <p><strong>Email:</strong> {{data.email}}</p>}}
          {{data?.status && <p><strong>Status:</strong> {{data.status}}</p>}}
          
          <details style={{{{ marginTop: '1rem' }}}}>
            <summary>Raw Data (Dev)</summary>
            <pre style={{{{ background: '#f5f5f5', padding: '1rem', overflow: 'auto' }}}}>
              {{JSON.stringify(data, null, 2)}}
            </pre>
          </details>
        </div>
      )}}
    </div>
  );
}};
'''
        # Save Component
        path = f'/home/runner/work/mrsunkwn/mrsunkwn/frontend/src/components/{component_name}.tsx'
        self._save_code(path, code)
        
    def _create_react_page(self, task):
        '''Generates React Page'''
        page_name = task.get('page_name', 'NewPage')
        code = f'''import React from 'react';
import {{ UserProfile }} from '../components/UserProfile';
import {{ LoadingSpinner }} from '../components/LoadingSpinner';

interface {page_name}Props {{
  className?: string;
}}

export const {page_name}: React.FC<{page_name}Props> = ({{ className }}) => {{
  return (
    <div className={{`{page_name.lower()}-page ${{className || ''}}`}}>
      <div className="page-header">
        <h1>{page_name}</h1>
        <p>Generated by Frontend Sprint Agent</p>
      </div>
      
      <div className="page-content">
        <div className="widget-grid">
          <div className="widget">
            <UserProfile />
          </div>
          
          <div className="widget">
            <h4>System Status</h4>
            <LoadingSpinner />
          </div>
          
          <div className="widget">
            <h4>Quick Actions</h4>
            <button onClick={{() => window.location.reload()}}>
              🔄 Refresh Data
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}};
'''
        path = f'/home/runner/work/mrsunkwn/mrsunkwn/frontend/src/pages/{page_name}.tsx'
        self._save_code(path, code)
        
    def _create_react_hook(self, task):
        '''Generates React Hook'''
        hook_name = task.get('hook_name', 'useNewHook')
        code = f'''import {{ useState, useEffect, useCallback }} from 'react';
import {{ apiClient }} from '../services/apiClient';

interface {hook_name}Options {{
  endpoint: string;
  autoRefresh?: boolean;
  refreshInterval?: number;
}}

interface {hook_name}Result<T> {{
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
  lastFetched: Date | null;
}}

export function {hook_name}<T = any>(
  options: {hook_name}Options
): {hook_name}Result<T> {{
  const {{ endpoint, autoRefresh = false, refreshInterval = 30000 }} = options;
  
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [lastFetched, setLastFetched] = useState<Date | null>(null);

  const fetchData = useCallback(async () => {{
    try {{
      setLoading(true);
      setError(null);
      const response = await apiClient.get(endpoint);
      setData(response.data);
      setLastFetched(new Date());
      console.log(`✅ {hook_name} fetched data from ${{endpoint}}`);
    }} catch (err) {{
      setError(err as Error);
      console.error(`❌ {hook_name} error:`, err);
    }} finally {{
      setLoading(false);
    }}
  }}, [endpoint]);

  useEffect(() => {{
    fetchData();
  }}, [fetchData]);

  useEffect(() => {{
    if (autoRefresh) {{
      const interval = setInterval(fetchData, refreshInterval);
      return () => clearInterval(interval);
    }}
  }}, [autoRefresh, refreshInterval, fetchData]);

  return {{ data, loading, error, refetch: fetchData, lastFetched }};
}}
'''
        path = f'/home/runner/work/mrsunkwn/mrsunkwn/frontend/src/hooks/{hook_name}.ts'
        self._save_code(path, code)
        
    def _create_loading_spinner_component(self, task):
        '''Creates a specialized loading spinner component'''
        code = '''import React from 'react';

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
'''
        path = '/home/runner/work/mrsunkwn/mrsunkwn/frontend/src/components/LoadingSpinner.tsx'
        self._save_code(path, code)
        
    def _create_api_endpoint(self, task):
        '''Generates API Endpoint'''
        # TODO: Implement API endpoint generation
        pass
        
    def _create_data_model(self, task):
        '''Generates Data Model'''
        # TODO: Implement data model generation
        pass
        
    def _create_service(self, task):
        '''Generates Service'''
        # TODO: Implement service generation
        pass
        
    def _save_code(self, path, code):
        '''Save generated code to file'''
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(code)
        print(f"✅ Saved: {path}")

# Sprint Executor
if __name__ == '__main__':
    agent = os.getenv('AGENT_ROLE', 'FRONTEND_AGENT')
    runner = SprintRunner(agent)
    runner.run_sprint()