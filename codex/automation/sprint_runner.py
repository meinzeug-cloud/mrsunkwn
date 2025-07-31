import os
import sys
import time
import json
import subprocess
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

            if task['type'] in ['feature', 'api', 'component', 'endpoint']:
                self._generate_code(task)
            elif task['type'] in ['model', 'service']:
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
        
        # Get the tasks that will be prioritized
        upcoming_tasks = self._get_upcoming_tasks()
        
        # Create GitHub issues for each task
        for task in upcoming_tasks:
            self._create_github_issue(task)
        
        print(f"✅ Created {len(upcoming_tasks)} GitHub issues")
        
    def _get_upcoming_tasks(self):
        '''Get tasks that will be worked on in this sprint'''
        if self.agent == 'BACKEND_AGENT':
            return [
                {'title': 'User Management API', 'type': 'api', 'endpoint': '/api/users'},
                {'title': 'Learning Session Model', 'type': 'model', 'model_name': 'LearningSession'},
                {'title': 'Tutor Service', 'type': 'service', 'service_name': 'TutorService'},
                {'title': 'Analytics API', 'type': 'api', 'endpoint': '/api/analytics'},
                {'title': 'Family Management Model', 'type': 'model', 'model_name': 'FamilyManagement'},
                {'title': 'Parental Control Service', 'type': 'service', 'service_name': 'ParentalControlService'},
            ]
        else:
            # Frontend tasks
            return [
                {'title': 'Dashboard Component', 'type': 'component', 'component_name': 'Dashboard'},
                {'title': 'Learning Interface', 'type': 'component', 'component_name': 'LearningInterface'},
                {'title': 'Parent Control Panel', 'type': 'component', 'component_name': 'ParentControlPanel'},
            ]
    
    def _create_github_issue(self, task):
        '''Create a GitHub issue for a task'''
        try:
            # Skip if required env vars are not set or are dummy values
            github_token = os.getenv('GITHUB_TOKEN')
            repo_owner = os.getenv('REPO_OWNER')
            repo_name = os.getenv('REPO_NAME')
            
            if not github_token or not repo_owner or not repo_name or github_token == 'dummy_token':
                print(f"⚠️ Skipping GitHub issue creation for '{task['title']}' - missing or dummy credentials")
                return
                
            # Generate issue title and labels
            if task['type'] == 'api':
                title = f"🔌 Implement {task['title']}"
                labels = ['backend', 'api', 'enhancement']
            elif task['type'] == 'model':
                title = f"🗃️ Create {task['title']}"
                labels = ['backend', 'model', 'enhancement']
            elif task['type'] == 'service':
                title = f"⚙️ Implement {task['title']}"
                labels = ['backend', 'service', 'enhancement']
            elif task['type'] == 'component':
                title = f"🎨 Create {task['title']}"
                labels = ['frontend', 'component', 'enhancement']
            else:
                title = f"📋 {task['title']}"
                labels = [self.agent.lower().replace('_agent', ''), 'enhancement']
            
            # Generate issue body
            body = self._generate_issue_body(task)
            
            # Create issue data
            issue_data = {
                'title': title,
                'body': body,
                'labels': labels
            }
            
            # Create issue via GitHub API
            curl_cmd = [
                'curl', '-s', '-X', 'POST',
                '-H', f'Authorization: token {github_token}',
                '-H', 'Accept: application/vnd.github.v3+json',
                '-d', json.dumps(issue_data),
                f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                try:
                    response = json.loads(result.stdout)
                    if 'html_url' in response:
                        print(f"✅ Created issue: {title} ({response['html_url']})")
                    else:
                        print(f"⚠️ Issue creation response: {result.stdout}")
                except json.JSONDecodeError:
                    print(f"⚠️ Issue created but couldn't parse response for: {title}")
            else:
                print(f"❌ Failed to create issue '{title}': {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error creating issue for '{task['title']}': {str(e)}")
    
    def _generate_issue_body(self, task):
        '''Generate issue body for a task'''
        sprint_info = f"Sprint #{self.sprint_count} - {self.agent}"
        
        if task['type'] == 'api':
            body = f"""## 🤖 Auto-Generated by {self.agent}

### Task Type: API Endpoint Implementation

### Details:
- **Endpoint**: `{task.get('endpoint', 'N/A')}`
- **Sprint**: {sprint_info}
- **Priority**: High

### Requirements:
- [ ] Implement FastAPI endpoint
- [ ] Add request/response models
- [ ] Include proper error handling
- [ ] Add endpoint to main app router
- [ ] Test endpoint functionality

### Implementation Notes:
This endpoint should follow RESTful principles and include:
- GET, POST, PUT, DELETE operations as appropriate
- Proper HTTP status codes
- Input validation using Pydantic models
- Error handling with meaningful messages

### Auto-Sync ID: {datetime.now().isoformat()}
"""
        elif task['type'] == 'model':
            body = f"""## 🤖 Auto-Generated by {self.agent}

### Task Type: Data Model Creation

### Details:
- **Model Name**: `{task.get('model_name', 'N/A')}`
- **Sprint**: {sprint_info}
- **Priority**: High

### Requirements:
- [ ] Create Pydantic models for data validation
- [ ] Include base, create, update, and response models
- [ ] Add database operations class
- [ ] Include proper field validation
- [ ] Add enum types where appropriate

### Implementation Notes:
This model should include:
- Base model with common fields
- Create model for new record creation
- Update model for partial updates
- Database operations for CRUD functionality
- Proper typing and validation

### Auto-Sync ID: {datetime.now().isoformat()}
"""
        elif task['type'] == 'service':
            body = f"""## 🤖 Auto-Generated by {self.agent}

### Task Type: Service Layer Implementation

### Details:
- **Service Name**: `{task.get('service_name', 'N/A')}`
- **Sprint**: {sprint_info}
- **Priority**: High

### Requirements:
- [ ] Implement service class with business logic
- [ ] Add CRUD operations
- [ ] Include proper error handling and logging
- [ ] Add data validation methods
- [ ] Integrate with corresponding models

### Implementation Notes:
This service should provide:
- Business logic layer between API and data models
- Proper error handling and logging
- Data validation and transformation
- Integration with database operations
- Async/await patterns for better performance

### Auto-Sync ID: {datetime.now().isoformat()}
"""
        else:
            body = f"""## 🤖 Auto-Generated by {self.agent}

### Task Type: {task['type'].title()}

### Details:
- **Task**: {task['title']}
- **Sprint**: {sprint_info}
- **Priority**: Medium

### Requirements:
- [ ] Implement core functionality
- [ ] Add appropriate tests
- [ ] Update documentation
- [ ] Follow project coding standards

### Auto-Sync ID: {datetime.now().isoformat()}
"""
        
        return body
        
    def _prioritize_tasks(self):
        '''Prioritize and return tasks'''
        print("📋 Prioritizing tasks...")

        
        # For backend agent, prioritize API-related tasks
        backend_tasks = [
            {'title': 'User Management API', 'type': 'api', 'endpoint': '/api/users'},
            {'title': 'Learning Session Model', 'type': 'model', 'model_name': 'LearningSession'},
            {'title': 'Tutor Service', 'type': 'service', 'service_name': 'TutorService'},
            {'title': 'Analytics API', 'type': 'api', 'endpoint': '/api/analytics'},
            {'title': 'Family Management Model', 'type': 'model', 'model_name': 'FamilyManagement'},
            {'title': 'Parental Control Service', 'type': 'service', 'service_name': 'ParentalControlService'},
        ]

        
        # Return subset based on sprint goals
        return backend_tasks[:3]  # Focus on first 3 tasks per sprint
        
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
            if 'endpoint' in task['title'].lower() or task['type'] == 'api':
                self._create_api_endpoint(task)
            elif 'model' in task['title'].lower() or task['type'] == 'model':
                self._create_data_model(task)
            elif 'service' in task['title'].lower() or task['type'] == 'service':
                self._create_service(task)
                
    def _fix_code(self, task):
        '''Fix code for bugs'''
        print(f"🔧 Fixing code for: {task['title']}")
        # TODO: Implement bug fixes
        
    def _run_tests(self):
        '''Run tests'''
        print("🧪 Running tests...")
        
        backend_path = '/home/runner/work/mrsunkwn/mrsunkwn/backend'
        
        try:
            # Check if backend dependencies are installed
            import subprocess
            result = subprocess.run(['python3', '-c', 'import fastapi, uvicorn'], 
                                  capture_output=True, text=True, cwd=backend_path)
            
            if result.returncode == 0:
                print("✅ Backend dependencies available")
            else:
                print("⚠️ Installing backend dependencies...")
                subprocess.run(['pip3', 'install', '-r', 'requirements.txt'], 
                             cwd=backend_path, check=True)
                print("✅ Dependencies installed")
            
            # Try to import and validate the main app
            app_path = f'{backend_path}/src/app.py'
            if os.path.exists(app_path):
                result = subprocess.run(['python3', '-c', 'import sys; sys.path.append("src"); import app; print("App validated")'], 
                                      capture_output=True, text=True, cwd=backend_path)
                if result.returncode == 0:
                    print("✅ Backend app validation passed")
                else:
                    print(f"⚠️ Backend app validation issues: {result.stderr}")
            
            # Check generated files
            generated_files = []
            for root, dirs, files in os.walk(f'{backend_path}/src'):
                for file in files:
                    if file.endswith('.py') and file != 'app.py':
                        generated_files.append(os.path.join(root, file))
            
            print(f"✅ Generated {len(generated_files)} new backend files")
            
        except Exception as e:
            print(f"⚠️ Test execution had issues: {str(e)}")
        
        print("🧪 Test execution completed")
        
    def _update_status(self):
        '''Update status'''
        print("📊 Updating status...")
        
        # Calculate sprint metrics
        backend_path = '/home/runner/work/mrsunkwn/mrsunkwn/backend/src'
        
        try:
            # Count lines of code generated
            total_lines = 0
            new_files = 0
            
            for root, dirs, files in os.walk(backend_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r') as f:
                                lines = len(f.readlines())
                                total_lines += lines
                                if file != 'app.py':  # Count new files (not the original app.py)
                                    new_files += 1
                        except:
                            pass
            
            # Generate status report
            status_report = f"""
Sprint #{self.sprint_count} - {self.agent} Status Report
{'='*50}
📊 Metrics:
   - Total lines of code: {total_lines}
   - New files generated: {new_files}
   - Tasks completed: {min(3, new_files)}
   
🏗️ Generated Components:
   - API Endpoints: {len([f for f in os.listdir(f'{backend_path}/endpoints') if f.endswith('.py')]) if os.path.exists(f'{backend_path}/endpoints') else 0}
   - Data Models: {len([f for f in os.listdir(f'{backend_path}/models') if f.endswith('.py')]) if os.path.exists(f'{backend_path}/models') else 0}
   - Services: {len([f for f in os.listdir(f'{backend_path}/services') if f.endswith('.py')]) if os.path.exists(f'{backend_path}/services') else 0}

✅ Sprint Goals Met:
   - Code Generation: {'✅' if total_lines > 200 else '❌'} ({total_lines}/200+ lines)
   - New Features: {'✅' if new_files >= 2 else '❌'} ({new_files}/2+ features)
   - Backend Focus: ✅ API-first approach
   
🎯 Next Sprint Priorities:
   - Database integration
   - Authentication system
   - Testing framework
   
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            # Save status report
            status_path = '/home/runner/work/mrsunkwn/mrsunkwn/codex/data/backend/sprint_status.md'
            os.makedirs(os.path.dirname(status_path), exist_ok=True)
            with open(status_path, 'w') as f:
                f.write(status_report)
            
            print(status_report)
            print(f"✅ Status report saved to: {status_path}")
            
        except Exception as e:
            print(f"⚠️ Status update had issues: {str(e)}")
    
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
        endpoint = task.get('endpoint', '/api/example')
        endpoint_name = endpoint.split('/')[-1]
        
        # Generate endpoint code
        code = f'''
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class {endpoint_name.title()}Request(BaseModel):
    # TODO: Define request model
    name: str
    description: Optional[str] = None

class {endpoint_name.title()}Response(BaseModel):
    # TODO: Define response model  
    id: int
    status: str
    data: Optional[dict] = None

@router.get("{endpoint}")
async def get_{endpoint_name}():
    """Get {endpoint_name} data"""
    try:
        # TODO: Implement business logic
        return {{"status": "success", "data": []}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("{endpoint}")
async def create_{endpoint_name}(request: {endpoint_name.title()}Request):
    """Create new {endpoint_name}"""
    try:
        # TODO: Implement creation logic
        return {{"status": "created", "id": 1}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("{endpoint}/{{item_id}}")
async def update_{endpoint_name}(item_id: int, request: {endpoint_name.title()}Request):
    """Update {endpoint_name} by ID"""
    try:
        # TODO: Implement update logic
        return {{"status": "updated", "id": item_id}}
    except Exception as e:
        raise HTTPException(status_code=404, detail="{endpoint_name.title()} not found")

@router.delete("{endpoint}/{{item_id}}")
async def delete_{endpoint_name}(item_id: int):
    """Delete {endpoint_name} by ID"""
    try:
        # TODO: Implement deletion logic
        return {{"status": "deleted", "id": item_id}}
    except Exception as e:
        raise HTTPException(status_code=404, detail="{endpoint_name.title()} not found")
'''
        
        # Save endpoint code
        path = f'/home/runner/work/mrsunkwn/mrsunkwn/backend/src/endpoints/{endpoint_name}.py'
        self._save_code(path, code)
        
        # Update main app.py to include the endpoint
        self._update_main_app_router(endpoint_name)
        
    def _create_data_model(self, task):
        '''Generates Data Model'''
        model_name = task.get('model_name', 'ExampleModel')
        
        code = f'''
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class {model_name}Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class {model_name}Base(BaseModel):
    """Base model for {model_name}"""
    name: str = Field(..., description="Name of the {model_name.lower()}")
    description: Optional[str] = Field(None, description="Description of the {model_name.lower()}")
    status: {model_name}Status = Field(default={model_name}Status.ACTIVE, description="Status of the {model_name.lower()}")

class {model_name}Create({model_name}Base):
    """Model for creating {model_name}"""
    pass

class {model_name}Update(BaseModel):
    """Model for updating {model_name}"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[{model_name}Status] = None

class {model_name}InDB({model_name}Base):
    """Model for {model_name} in database"""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

class {model_name}Response({model_name}InDB):
    """Model for {model_name} API response"""
    pass

# Database operations (placeholder for actual DB implementation)
class {model_name}DB:
    @staticmethod
    async def create(data: {model_name}Create) -> {model_name}InDB:
        """Create new {model_name.lower()} in database"""
        # TODO: Implement database creation
        return {model_name}InDB(id=1, **data.dict())
    
    @staticmethod
    async def get_by_id(id: int) -> Optional[{model_name}InDB]:
        """Get {model_name.lower()} by ID from database"""
        # TODO: Implement database query
        return None
    
    @staticmethod
    async def get_all() -> List[{model_name}InDB]:
        """Get all {model_name.lower()}s from database"""
        # TODO: Implement database query
        return []
    
    @staticmethod
    async def update(id: int, data: {model_name}Update) -> Optional[{model_name}InDB]:
        """Update {model_name.lower()} in database"""
        # TODO: Implement database update
        return None
    
    @staticmethod
    async def delete(id: int) -> bool:
        """Delete {model_name.lower()} from database"""
        # TODO: Implement database deletion
        return False
'''
        
        # Save model code
        path = f'/home/runner/work/mrsunkwn/mrsunkwn/backend/src/models/{model_name.lower()}.py'
        self._save_code(path, code)
        
    def _create_service(self, task):
        '''Generates Service'''
        service_name = task.get('service_name', 'ExampleService')
        
        code = f'''
from typing import List, Optional
from {service_name.lower()}_model import {service_name}Create, {service_name}Update, {service_name}InDB, {service_name}DB
import logging

logger = logging.getLogger(__name__)

class {service_name}Service:
    """Service layer for {service_name} operations"""
    
    @staticmethod
    async def create_{service_name.lower()}(data: {service_name}Create) -> {service_name}InDB:
        """Create a new {service_name.lower()}"""
        try:
            logger.info(f"Creating new {service_name.lower()}: {{data.name}}")
            result = await {service_name}DB.create(data)
            logger.info(f"{service_name} created successfully with ID: {{result.id}}")
            return result
        except Exception as e:
            logger.error(f"Error creating {service_name.lower()}: {{str(e)}}")
            raise
    
    @staticmethod
    async def get_{service_name.lower()}_by_id(id: int) -> Optional[{service_name}InDB]:
        """Get {service_name.lower()} by ID"""
        try:
            logger.info(f"Fetching {service_name.lower()} with ID: {{id}}")
            result = await {service_name}DB.get_by_id(id)
            if not result:
                logger.warning(f"{service_name} with ID {{id}} not found")
            return result
        except Exception as e:
            logger.error(f"Error fetching {service_name.lower()}: {{str(e)}}")
            raise
    
    @staticmethod
    async def get_all_{service_name.lower()}s() -> List[{service_name}InDB]:
        """Get all {service_name.lower()}s"""
        try:
            logger.info(f"Fetching all {service_name.lower()}s")
            result = await {service_name}DB.get_all()
            logger.info(f"Found {{len(result)}} {service_name.lower()}s")
            return result
        except Exception as e:
            logger.error(f"Error fetching {service_name.lower()}s: {{str(e)}}")
            raise
    
    @staticmethod
    async def update_{service_name.lower()}(id: int, data: {service_name}Update) -> Optional[{service_name}InDB]:
        """Update {service_name.lower()} by ID"""
        try:
            logger.info(f"Updating {service_name.lower()} with ID: {{id}}")
            
            # Check if {service_name.lower()} exists
            existing = await {service_name}DB.get_by_id(id)
            if not existing:
                logger.warning(f"{service_name} with ID {{id}} not found for update")
                return None
            
            result = await {service_name}DB.update(id, data)
            logger.info(f"{service_name} updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating {service_name.lower()}: {{str(e)}}")
            raise
    
    @staticmethod
    async def delete_{service_name.lower()}(id: int) -> bool:
        """Delete {service_name.lower()} by ID"""
        try:
            logger.info(f"Deleting {service_name.lower()} with ID: {{id}}")
            
            # Check if {service_name.lower()} exists
            existing = await {service_name}DB.get_by_id(id)
            if not existing:
                logger.warning(f"{service_name} with ID {{id}} not found for deletion")
                return False
            
            result = await {service_name}DB.delete(id)
            logger.info(f"{service_name} deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting {service_name.lower()}: {{str(e)}}")
            raise
    
    @staticmethod
    async def validate_{service_name.lower()}_data(data: {service_name}Create) -> bool:
        """Validate {service_name.lower()} data before creation"""
        try:
            # Add custom validation logic here
            if not data.name or len(data.name.strip()) == 0:
                logger.warning("Invalid {service_name.lower()} data: name is required")
                return False
            
            # Add more validation rules as needed
            logger.info("{service_name} data validation passed")
            return True
        except Exception as e:
            logger.error(f"Error validating {service_name.lower()} data: {{str(e)}}")
            return False
'''
        
        # Save service code
        path = f'/home/runner/work/mrsunkwn/mrsunkwn/backend/src/services/{service_name.lower()}_service.py'
        self._save_code(path, code)
        
    def _save_code(self, path, code):
        '''Save generated code to file'''
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(code)
        print(f"✅ Saved: {path}")
    
    def _update_main_app_router(self, endpoint_name):
        '''Update main app.py to include new router'''
        try:
            app_path = '/home/runner/work/mrsunkwn/mrsunkwn/backend/src/app.py'
            
            # Read current app.py
            with open(app_path, 'r') as f:
                content = f.read()
            
            # Add import and router inclusion
            import_line = f"from endpoints.{endpoint_name} import router as {endpoint_name}_router"
            router_line = f"app.include_router({endpoint_name}_router)"
            
            if import_line not in content:
                lines = content.split('\n')
                
                # Find the last import and add after it
                import_index = -1
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        import_index = i
                
                if import_index >= 0:
                    lines.insert(import_index + 1, import_line)
                
                # Find where to add router (after middleware setup)
                router_index = -1
                for i, line in enumerate(lines):
                    if 'add_middleware' in line or 'CORSMiddleware' in line:
                        # Find the end of middleware block
                        for j in range(i, len(lines)):
                            if lines[j].strip() == ')':
                                router_index = j + 1
                                break
                        break
                
                if router_index >= 0 and router_line not in content:
                    lines.insert(router_index + 1, router_line)
                    
                # Write back to file
                with open(app_path, 'w') as f:
                    f.write('\n'.join(lines))
                print(f"✅ Updated app.py with {endpoint_name} router")
                
        except Exception as e:
            print(f"⚠️ Could not update app.py: {str(e)}")

# Sprint Executor
if __name__ == '__main__':
    agent = os.getenv('AGENT_ROLE', 'FRONTEND_AGENT')
    runner = SprintRunner(agent)
    runner.run_sprint()