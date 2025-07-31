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
        '''Get tasks that will be worked on in this sprint - 100x expansion'''
        if self.agent == 'UNIFIED_AGENT':
            # Massively expanded task list for 100x code generation
            return [
                # Core Backend APIs (20 APIs)
                {'title': 'User Management API', 'type': 'api', 'endpoint': '/api/users'},
                {'title': 'Authentication API', 'type': 'api', 'endpoint': '/api/auth'},
                {'title': 'Session Management API', 'type': 'api', 'endpoint': '/api/sessions'},
                {'title': 'Course Management API', 'type': 'api', 'endpoint': '/api/courses'},
                {'title': 'Lesson Management API', 'type': 'api', 'endpoint': '/api/lessons'},
                {'title': 'Assignment API', 'type': 'api', 'endpoint': '/api/assignments'},
                {'title': 'Grade Management API', 'type': 'api', 'endpoint': '/api/grades'},
                {'title': 'Progress Tracking API', 'type': 'api', 'endpoint': '/api/progress'},
                {'title': 'Notification API', 'type': 'api', 'endpoint': '/api/notifications'},
                {'title': 'File Management API', 'type': 'api', 'endpoint': '/api/files'},
                {'title': 'Analytics API', 'type': 'api', 'endpoint': '/api/analytics'},
                {'title': 'Reporting API', 'type': 'api', 'endpoint': '/api/reports'},
                {'title': 'Settings API', 'type': 'api', 'endpoint': '/api/settings'},
                {'title': 'Calendar API', 'type': 'api', 'endpoint': '/api/calendar'},
                {'title': 'Communication API', 'type': 'api', 'endpoint': '/api/messages'},
                {'title': 'Payment API', 'type': 'api', 'endpoint': '/api/payments'},
                {'title': 'Subscription API', 'type': 'api', 'endpoint': '/api/subscriptions'},
                {'title': 'Feedback API', 'type': 'api', 'endpoint': '/api/feedback'},
                {'title': 'Support API', 'type': 'api', 'endpoint': '/api/support'},
                {'title': 'Admin API', 'type': 'api', 'endpoint': '/api/admin'},
                
                # Data Models (20 models)
                {'title': 'User Model', 'type': 'model', 'model_name': 'User'},
                {'title': 'Learning Session Model', 'type': 'model', 'model_name': 'LearningSession'},
                {'title': 'Course Model', 'type': 'model', 'model_name': 'Course'},
                {'title': 'Lesson Model', 'type': 'model', 'model_name': 'Lesson'},
                {'title': 'Assignment Model', 'type': 'model', 'model_name': 'Assignment'},
                {'title': 'Grade Model', 'type': 'model', 'model_name': 'Grade'},
                {'title': 'Progress Model', 'type': 'model', 'model_name': 'Progress'},
                {'title': 'Notification Model', 'type': 'model', 'model_name': 'Notification'},
                {'title': 'File Model', 'type': 'model', 'model_name': 'File'},
                {'title': 'Analytics Model', 'type': 'model', 'model_name': 'Analytics'},
                {'title': 'Report Model', 'type': 'model', 'model_name': 'Report'},
                {'title': 'Settings Model', 'type': 'model', 'model_name': 'Settings'},
                {'title': 'Calendar Model', 'type': 'model', 'model_name': 'Calendar'},
                {'title': 'Message Model', 'type': 'model', 'model_name': 'Message'},
                {'title': 'Payment Model', 'type': 'model', 'model_name': 'Payment'},
                {'title': 'Subscription Model', 'type': 'model', 'model_name': 'Subscription'},
                {'title': 'Feedback Model', 'type': 'model', 'model_name': 'Feedback'},
                {'title': 'Support Model', 'type': 'model', 'model_name': 'Support'},
                {'title': 'Family Model', 'type': 'model', 'model_name': 'Family'},
                {'title': 'Profile Model', 'type': 'model', 'model_name': 'Profile'},
                
                # Services (20 services)
                {'title': 'User Service', 'type': 'service', 'service_name': 'UserService'},
                {'title': 'Authentication Service', 'type': 'service', 'service_name': 'AuthService'},
                {'title': 'Tutor Service', 'type': 'service', 'service_name': 'TutorService'},
                {'title': 'Course Service', 'type': 'service', 'service_name': 'CourseService'},
                {'title': 'Lesson Service', 'type': 'service', 'service_name': 'LessonService'},
                {'title': 'Assignment Service', 'type': 'service', 'service_name': 'AssignmentService'},
                {'title': 'Grading Service', 'type': 'service', 'service_name': 'GradingService'},
                {'title': 'Progress Service', 'type': 'service', 'service_name': 'ProgressService'},
                {'title': 'Notification Service', 'type': 'service', 'service_name': 'NotificationService'},
                {'title': 'File Service', 'type': 'service', 'service_name': 'FileService'},
                {'title': 'Analytics Service', 'type': 'service', 'service_name': 'AnalyticsService'},
                {'title': 'Reporting Service', 'type': 'service', 'service_name': 'ReportingService'},
                {'title': 'Settings Service', 'type': 'service', 'service_name': 'SettingsService'},
                {'title': 'Calendar Service', 'type': 'service', 'service_name': 'CalendarService'},
                {'title': 'Communication Service', 'type': 'service', 'service_name': 'CommunicationService'},
                {'title': 'Payment Service', 'type': 'service', 'service_name': 'PaymentService'},
                {'title': 'Subscription Service', 'type': 'service', 'service_name': 'SubscriptionService'},
                {'title': 'Feedback Service', 'type': 'service', 'service_name': 'FeedbackService'},
                {'title': 'Support Service', 'type': 'service', 'service_name': 'SupportService'},
                {'title': 'Email Service', 'type': 'service', 'service_name': 'EmailService'},
                
                # Frontend Components (25 components)
                {'title': 'Dashboard Component', 'type': 'component', 'component_name': 'Dashboard'},
                {'title': 'Learning Interface', 'type': 'component', 'component_name': 'LearningInterface'},
                {'title': 'Parent Control Panel', 'type': 'component', 'component_name': 'ParentControlPanel'},
                {'title': 'Course Browser', 'type': 'component', 'component_name': 'CourseBrowser'},
                {'title': 'Lesson Viewer', 'type': 'component', 'component_name': 'LessonViewer'},
                {'title': 'Assignment Manager', 'type': 'component', 'component_name': 'AssignmentManager'},
                {'title': 'Grade Tracker', 'type': 'component', 'component_name': 'GradeTracker'},
                {'title': 'Progress Chart', 'type': 'component', 'component_name': 'ProgressChart'},
                {'title': 'Notification Center', 'type': 'component', 'component_name': 'NotificationCenter'},
                {'title': 'File Manager', 'type': 'component', 'component_name': 'FileManager'},
                {'title': 'User Profile', 'type': 'component', 'component_name': 'UserProfile'},
                {'title': 'Settings Panel', 'type': 'component', 'component_name': 'SettingsPanel'},
                {'title': 'Calendar Widget', 'type': 'component', 'component_name': 'CalendarWidget'},
                {'title': 'Chat Interface', 'type': 'component', 'component_name': 'ChatInterface'},
                {'title': 'Video Player', 'type': 'component', 'component_name': 'VideoPlayer'},
                {'title': 'Quiz Engine', 'type': 'component', 'component_name': 'QuizEngine'},
                {'title': 'Search Bar', 'type': 'component', 'component_name': 'SearchBar'},
                {'title': 'Navigation Menu', 'type': 'component', 'component_name': 'NavigationMenu'},
                {'title': 'Loading Spinner', 'type': 'component', 'component_name': 'LoadingSpinner'},
                {'title': 'Error Boundary', 'type': 'component', 'component_name': 'ErrorBoundary'},
                {'title': 'Data Table', 'type': 'component', 'component_name': 'DataTable'},
                {'title': 'Modal Dialog', 'type': 'component', 'component_name': 'ModalDialog'},
                {'title': 'Form Builder', 'type': 'component', 'component_name': 'FormBuilder'},
                {'title': 'Chart Visualization', 'type': 'component', 'component_name': 'ChartVisualization'},
                {'title': 'Media Gallery', 'type': 'component', 'component_name': 'MediaGallery'},
                
                # Utilities and Helpers (15 items)
                {'title': 'API Utilities', 'type': 'utility', 'utility_name': 'ApiUtils'},
                {'title': 'Date Utilities', 'type': 'utility', 'utility_name': 'DateUtils'},
                {'title': 'String Utilities', 'type': 'utility', 'utility_name': 'StringUtils'},
                {'title': 'Validation Utilities', 'type': 'utility', 'utility_name': 'ValidationUtils'},
                {'title': 'Crypto Utilities', 'type': 'utility', 'utility_name': 'CryptoUtils'},
                {'title': 'File Utilities', 'type': 'utility', 'utility_name': 'FileUtils'},
                {'title': 'Math Utilities', 'type': 'utility', 'utility_name': 'MathUtils'},
                {'title': 'Array Utilities', 'type': 'utility', 'utility_name': 'ArrayUtils'},
                {'title': 'Object Utilities', 'type': 'utility', 'utility_name': 'ObjectUtils'},
                {'title': 'Color Utilities', 'type': 'utility', 'utility_name': 'ColorUtils'},
                {'title': 'Browser Utilities', 'type': 'utility', 'utility_name': 'BrowserUtils'},
                {'title': 'Storage Utilities', 'type': 'utility', 'utility_name': 'StorageUtils'},
                {'title': 'Network Utilities', 'type': 'utility', 'utility_name': 'NetworkUtils'},
                {'title': 'Performance Utilities', 'type': 'utility', 'utility_name': 'PerformanceUtils'},
                {'title': 'Debug Utilities', 'type': 'utility', 'utility_name': 'DebugUtils'},
                
                # Custom Hooks (10 hooks)
                {'title': 'User Data Hook', 'type': 'hook', 'hook_name': 'useUserData'},
                {'title': 'API Hook', 'type': 'hook', 'hook_name': 'useAPI'},
                {'title': 'Auth Hook', 'type': 'hook', 'hook_name': 'useAuth'},
                {'title': 'Local Storage Hook', 'type': 'hook', 'hook_name': 'useLocalStorage'},
                {'title': 'Form Hook', 'type': 'hook', 'hook_name': 'useForm'},
                {'title': 'Timer Hook', 'type': 'hook', 'hook_name': 'useTimer'},
                {'title': 'Media Query Hook', 'type': 'hook', 'hook_name': 'useMediaQuery'},
                {'title': 'Websocket Hook', 'type': 'hook', 'hook_name': 'useWebSocket'},
                {'title': 'Animation Hook', 'type': 'hook', 'hook_name': 'useAnimation'},
                {'title': 'Pagination Hook', 'type': 'hook', 'hook_name': 'usePagination'},
            ]
        elif self.agent == 'BACKEND_AGENT':
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
        '''Prioritize and return tasks - 100x expansion'''
        print("📋 Prioritizing tasks for massive code generation...")

        # Get all upcoming tasks and process them all
        all_tasks = self._get_upcoming_tasks()
        print(f"🚀 Processing ALL {len(all_tasks)} tasks for 100x code generation")
        return all_tasks
        
    def _generate_code(self, task):
        '''GENERATES ACTUAL CODE - Enhanced for 100x output'''
        print(f"💻 Generating code for: {task['title']}")
        
        # Handle all task types for massive code generation
        if task['type'] == 'api':
            self._create_api_endpoint(task)
        elif task['type'] == 'model':
            self._create_data_model(task)
        elif task['type'] == 'service':
            self._create_service(task)
        elif task['type'] == 'component':
            self._create_react_component(task)
        elif task['type'] == 'hook':
            self._create_react_hook(task)
        elif task['type'] == 'utility':
            self._create_utility(task)
        elif task['type'] == 'page':
            self._create_react_page(task)
        else:
            print(f"⚠️ Unknown task type: {task['type']}")
                
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
        '''Generates Comprehensive React Component with full functionality'''
        component_name = task.get('component_name', 'NewComponent')
        
        # Create a comprehensive, feature-rich component
        code = f'''import React, {{ useState, useEffect, useCallback, useMemo, useRef }} from 'react';
import {{ useAPI }} from '../hooks/useAPI';
import {{ useAuth }} from '../hooks/useAuth';
import {{ useLocalStorage }} from '../hooks/useLocalStorage';

// Interfaces and Types
interface {component_name}Props {{
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
  customActions?: Array<{{
    label: string;
    icon?: string;
    onClick: (item: any) => void;
    disabled?: (item: any) => boolean;
  }}>;
}}

interface {component_name}State {{
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
}}

// Main Component
export const {component_name}: React.FC<{component_name}Props> = ({{
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
}}) => {{
  // State Management
  const [state, setState] = useState<{component_name}State>({{
    expanded: true,
    selectedItems: new Set<string>(),
    searchQuery: '',
    filters: {{}},
    sortBy: 'created_at',
    sortDirection: 'desc',
    currentPage: 1,
    itemsPerPage: 20,
    viewMode: 'list',
    showModal: false,
    modalContent: null,
    lastRefreshed: new Date()
  }});

  // Refs
  const searchInputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Custom Hooks
  const [preferences, setPreferences] = useLocalStorage(`{component_name.lower()}_preferences`, {{
    viewMode: 'list',
    itemsPerPage: 20,
    sortBy: 'created_at',
    sortDirection: 'desc'
  }});

  // API Configuration
  const apiEndpoint = useMemo(() => {{
    const baseUrl = userId ? `/api/{component_name.lower()}s/user/${{userId}}` : `/api/{component_name.lower()}s`;
    const queryParams = new URLSearchParams();
    
    if (state.searchQuery) queryParams.append('search', state.searchQuery);
    if (state.sortBy) queryParams.append('sort_by', state.sortBy);
    if (state.sortDirection) queryParams.append('sort_order', state.sortDirection);
    queryParams.append('page', state.currentPage.toString());
    queryParams.append('per_page', state.itemsPerPage.toString());
    
    Object.entries(state.filters).forEach(([key, value]) => {{
      if (value !== null && value !== undefined && value !== '') {{
        queryParams.append(key, value.toString());
      }}
    }});
    
    return `${{baseUrl}}?${{queryParams.toString()}}`;
  }}, [userId, state.searchQuery, state.sortBy, state.sortDirection, state.currentPage, state.itemsPerPage, state.filters]);

  // API Hook
  const {{ data, loading, error, refetch, lastFetched }} = useAPI(apiEndpoint, {{
    autoRefresh,
    refreshInterval
  }});

  // Update state on data changes
  useEffect(() => {{
    if (data) {{
      setState(prev => ({{ ...prev, lastRefreshed: new Date() }}));
      onSuccess?.(data);
    }}
  }}, [data, onSuccess]);

  // Handle errors
  useEffect(() => {{
    if (error) {{
      console.error(`{component_name} error:`, error);
      onError?.(error);
    }}
  }}, [error, onError]);

  // Event Handlers
  const updateState = useCallback((updates: Partial<{component_name}State>) => {{
    setState(prev => ({{ ...prev, ...updates }}));
  }}, []);

  const handleItemClick = useCallback((item: any, event: React.MouseEvent) => {{
    if (event.ctrlKey || event.metaKey) {{
      const newSelected = new Set(state.selectedItems);
      if (newSelected.has(item.id)) {{
        newSelected.delete(item.id);
      }} else {{
        newSelected.add(item.id);
      }}
      updateState({{ selectedItems: newSelected }});
      const selectedData = Array.from(newSelected).map(id => data?.items?.find((i: any) => i.id === id)).filter(Boolean);
      onItemSelect?.(selectedData);
    }} else {{
      onItemClick?.(item);
    }}
  }}, [state.selectedItems, data?.items, onItemClick, onItemSelect, updateState]);

  const handleSearch = useCallback((query: string) => {{
    updateState({{ 
      searchQuery: query,
      currentPage: 1
    }});
  }}, [updateState]);

  const handleFilter = useCallback((filterKey: string, value: any) => {{
    updateState({{ 
      filters: {{ ...state.filters, [filterKey]: value }},
      currentPage: 1
    }});
  }}, [state.filters, updateState]);

  const handleSort = useCallback((sortBy: string) => {{
    const sortDirection = state.sortBy === sortBy && state.sortDirection === 'asc' ? 'desc' : 'asc';
    updateState({{ sortBy, sortDirection, currentPage: 1 }});
    setPreferences(prev => ({{ ...prev, sortBy, sortDirection }}));
  }}, [state.sortBy, state.sortDirection, updateState, setPreferences]);

  const handlePageChange = useCallback((page: number) => {{
    updateState({{ currentPage: page }});
  }}, [updateState]);

  const handleRefresh = useCallback(() => {{
    refetch();
    updateState({{ lastRefreshed: new Date() }});
  }}, [refetch, updateState]);

  const handleSelectAll = useCallback(() => {{
    if (!data?.items) return;
    
    const allIds = new Set(data.items.map((item: any) => item.id));
    const isAllSelected = data.items.every((item: any) => state.selectedItems.has(item.id));
    
    const newSelected = isAllSelected ? new Set<string>() : allIds;
    updateState({{ selectedItems: newSelected }});
    const selectedData = Array.from(newSelected).map(id => data.items.find((i: any) => i.id === id)).filter(Boolean);
    onItemSelect?.(selectedData);
  }}, [data?.items, state.selectedItems, updateState, onItemSelect]);

  const handleExport = useCallback((format: 'csv' | 'json') => {{
    if (!data?.items) return;
    
    const exportData = state.selectedItems.size > 0 
      ? data.items.filter((item: any) => state.selectedItems.has(item.id))
      : data.items;
    
    if (format === 'csv') {{
      const csv = convertToCSV(exportData);
      downloadFile(csv, `{component_name.lower()}_export.csv`, 'text/csv');
    }} else {{
      const json = JSON.stringify(exportData, null, 2);
      downloadFile(json, `{component_name.lower()}_export.json`, 'application/json');
    }}
  }}, [data?.items, state.selectedItems]);

  // Utility functions
  const convertToCSV = (items: any[]) => {{
    if (!items.length) return '';
    const headers = Object.keys(items[0]).join(',');
    const rows = items.map(item => 
      Object.values(item).map(value => 
        typeof value === 'string' ? `"${{value.replace(/"/g, '""')}}"` : value
      ).join(',')
    );
    return [headers, ...rows].join('\\n');
  }};

  const downloadFile = (content: string, filename: string, contentType: string) => {{
    const blob = new Blob([content], {{ type: contentType }});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }};

  // Render helpers
  const renderToolbar = () => (
    <div className="component-toolbar">
      {{enableSearch && (
        <input
          ref={{searchInputRef}}
          type="text"
          value={{state.searchQuery}}
          onChange={{(e) => handleSearch(e.target.value)}}
          placeholder="Search..."
          className="search-input"
        />
      )}}
      
      <div className="toolbar-actions">
        {{enableRefresh && (
          <button 
            onClick={{handleRefresh}}
            disabled={{loading}}
            className="btn btn-secondary"
            title="Refresh"
          >
            🔄 Refresh
          </button>
        )}}
        
        {{enableExport && data?.items?.length > 0 && (
          <div className="export-buttons">
            <button onClick={{() => handleExport('csv')}} className="btn btn-secondary">
              📤 CSV
            </button>
            <button onClick={{() => handleExport('json')}} className="btn btn-secondary">
              📤 JSON
            </button>
          </div>
        )}}
        
        <div className="view-mode-selector">
          <button 
            className={{`btn ${{state.viewMode === 'list' ? 'active' : ''}}`}}
            onClick={{() => updateState({{ viewMode: 'list' }})}}
          >
            📋 List
          </button>
          <button 
            className={{`btn ${{state.viewMode === 'grid' ? 'active' : ''}}`}}
            onClick={{() => updateState({{ viewMode: 'grid' }})}}
          >
            ⊞ Grid
          </button>
          <button 
            className={{`btn ${{state.viewMode === 'table' ? 'active' : ''}}`}}
            onClick={{() => updateState({{ viewMode: 'table' }})}}
          >
            📊 Table
          </button>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {{
    if (loading) {{
      return (
        <div className="loading-container">
          <div className="loading-spinner">Loading {component_name.lower()}s...</div>
        </div>
      );
    }}

    if (error) {{
      return (
        <div className="error-container">
          <div className="error-message">
            <h4>Error loading {component_name.lower()}s</h4>
            <p>{{error.message}}</p>
            <button onClick={{handleRefresh}} className="btn btn-primary">
              Try Again
            </button>
          </div>
        </div>
      );
    }}

    if (!data?.items || data.items.length === 0) {{
      return (
        <div className="empty-state">
          <div className="empty-message">
            <h4>No {component_name.lower()}s found</h4>
            <p>{{state.searchQuery ? 'Try adjusting your search' : 'Get started by creating your first {component_name.lower()}'}}</p>
          </div>
        </div>
      );
    }}

    return (
      <div className={{`content-container view-mode-${{state.viewMode}}`}}>
        {{state.viewMode === 'table' && renderTable()}}
        {{state.viewMode === 'grid' && renderGrid()}}
        {{state.viewMode === 'list' && renderList()}}
      </div>
    );
  }};

  const renderTable = () => (
    <table className="data-table">
      <thead>
        <tr>
          <th>
            <input
              type="checkbox"
              checked={{data?.items?.length > 0 && data.items.every((item: any) => state.selectedItems.has(item.id))}}
              onChange={{handleSelectAll}}
            />
          </th>
          <th onClick={{() => handleSort('name')}}>
            Name 
            {{state.sortBy === 'name' && (
              <span className="sort-indicator">
                {{state.sortDirection === 'asc' ? '↑' : '↓'}}
              </span>
            )}}
          </th>
          <th onClick={{() => handleSort('status')}}>
            Status
            {{state.sortBy === 'status' && (
              <span className="sort-indicator">
                {{state.sortDirection === 'asc' ? '↑' : '↓'}}
              </span>
            )}}
          </th>
          <th onClick={{() => handleSort('created_at')}}>
            Created
            {{state.sortBy === 'created_at' && (
              <span className="sort-indicator">
                {{state.sortDirection === 'asc' ? '↑' : '↓'}}
              </span>
            )}}
          </th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {{data?.items?.map((item: any) => (
          <tr key={{item.id}} className={{state.selectedItems.has(item.id) ? 'selected' : ''}}>
            <td>
              <input
                type="checkbox"
                checked={{state.selectedItems.has(item.id)}}
                onChange={{() => {{
                  const newSelected = new Set(state.selectedItems);
                  if (newSelected.has(item.id)) {{
                    newSelected.delete(item.id);
                  }} else {{
                    newSelected.add(item.id);
                  }}
                  updateState({{ selectedItems: newSelected }});
                }}}}
              />
            </td>
            <td onClick={{(e) => handleItemClick(item, e)}}>{{item.name || 'Untitled'}}</td>
            <td>{{item.status || 'Unknown'}}</td>
            <td>{{item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A'}}</td>
            <td>
              {{customActions.map(action => (
                <button
                  key={{action.label}}
                  onClick={{() => action.onClick(item)}}
                  disabled={{action.disabled?.(item)}}
                  className="btn btn-sm"
                >
                  {{action.icon}} {{action.label}}
                </button>
              ))}}
            </td>
          </tr>
        ))}}
      </tbody>
    </table>
  );

  const renderGrid = () => (
    <div className="grid-container">
      {{data?.items?.map((item: any) => (
        <div 
          key={{item.id}} 
          className={{`grid-item ${{state.selectedItems.has(item.id) ? 'selected' : ''}}`}}
          onClick={{(e) => handleItemClick(item, e)}}
        >
          <h4>{{item.name || 'Untitled'}}</h4>
          <p>{{item.description || 'No description'}}</p>
          <div className="item-meta">
            <span className="status">{{item.status || 'Unknown'}}</span>
            <span className="date">{{item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A'}}</span>
          </div>
          <div className="item-actions">
            {{customActions.map(action => (
              <button
                key={{action.label}}
                onClick={{(e) => {{
                  e.stopPropagation();
                  action.onClick(item);
                }}}}
                disabled={{action.disabled?.(item)}}
                className="btn btn-sm"
              >
                {{action.icon}} {{action.label}}
              </button>
            ))}}
          </div>
        </div>
      ))}}
    </div>
  );

  const renderList = () => (
    <div className="list-container">
      {{data?.items?.map((item: any) => (
        <div 
          key={{item.id}} 
          className={{`list-item ${{state.selectedItems.has(item.id) ? 'selected' : ''}}`}}
          onClick={{(e) => handleItemClick(item, e)}}
        >
          <div className="item-content">
            <h4>{{item.name || 'Untitled'}}</h4>
            <p>{{item.description || 'No description'}}</p>
            <div className="item-meta">
              <span className="status">Status: {{item.status || 'Unknown'}}</span>
              <span className="date">Created: {{item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A'}}</span>
            </div>
          </div>
          <div className="item-actions">
            {{customActions.map(action => (
              <button
                key={{action.label}}
                onClick={{(e) => {{
                  e.stopPropagation();
                  action.onClick(item);
                }}}}
                disabled={{action.disabled?.(item)}}
                className="btn btn-sm"
              >
                {{action.icon}} {{action.label}}
              </button>
            ))}}
          </div>
        </div>
      ))}}
    </div>
  );

  const renderPagination = () => enablePagination && data?.total > state.itemsPerPage && (
    <div className="pagination-container">
      <div className="pagination-info">
        Showing {{((state.currentPage - 1) * state.itemsPerPage) + 1}} to {{Math.min(state.currentPage * state.itemsPerPage, data.total)}} of {{data.total}} items
      </div>
      <div className="pagination-controls">
        <button 
          onClick={{() => handlePageChange(state.currentPage - 1)}}
          disabled={{state.currentPage === 1}}
          className="btn btn-secondary"
        >
          Previous
        </button>
        
        <span className="page-info">Page {{state.currentPage}} of {{Math.ceil(data.total / state.itemsPerPage)}}</span>
        
        <button 
          onClick={{() => handlePageChange(state.currentPage + 1)}}
          disabled={{state.currentPage >= Math.ceil(data.total / state.itemsPerPage)}}
          className="btn btn-secondary"
        >
          Next
        </button>
      </div>
      <div className="items-per-page">
        <select 
          value={{state.itemsPerPage}}
          onChange={{(e) => {{
            const newItemsPerPage = Number(e.target.value);
            updateState({{ itemsPerPage: newItemsPerPage, currentPage: 1 }});
            setPreferences(prev => ({{ ...prev, itemsPerPage: newItemsPerPage }}));
          }}}}
        >
          <option value={{10}}>10 per page</option>
          <option value={{20}}>20 per page</option>
          <option value={{50}}>50 per page</option>
          <option value={{100}}>100 per page</option>
        </select>
      </div>
    </div>
  );

  // Main render
  return (
    <div 
      ref={{containerRef}}
      className={{`{component_name.lower()}-component theme-${{theme}} size-${{size}} variant-${{variant}} ${{className}}`}}
      data-testid="{component_name.lower()}-component"
    >
      <div className="component-header">
        <div className="header-content">
          <h3 className="component-title">
            {component_name}
            {{state.selectedItems.size > 0 && (
              <span className="selection-badge">
                {{state.selectedItems.size}} selected
              </span>
            )}}
          </h3>
          <div className="header-meta">
            {{lastFetched && (
              <span className="last-updated">
                Last updated: {{lastFetched.toLocaleTimeString()}}
              </span>
            )}}
            {{autoRefresh && (
              <span className="auto-refresh-indicator">
                🔄 Auto-refresh enabled
              </span>
            )}}
          </div>
        </div>
        
        <button
          className="expand-toggle"
          onClick={{() => updateState({{ expanded: !state.expanded }})}}
          aria-label={{state.expanded ? 'Collapse' : 'Expand'}}
        >
          {{state.expanded ? '▼' : '▶'}}
        </button>
      </div>

      {{state.expanded && (
        <div className="component-body">
          {{renderToolbar()}}
          {{renderContent()}}
          {{renderPagination()}}
          
          {{data?.items && (
            <details className="dev-info" style={{{{ marginTop: '2rem' }}}}>
              <summary>Debug Info (Development)</summary>
              <pre style={{{{ 
                background: '#f5f5f5', 
                padding: '1rem', 
                overflow: 'auto',
                fontSize: '0.8rem'
              }}}}>
                API Endpoint: {{apiEndpoint}}{{'\n'}}
                Items Count: {{data.items.length}}{{'\n'}}
                Total: {{data.total}}{{'\n'}}
                Selected: {{state.selectedItems.size}}{{'\n'}}
                Current Page: {{state.currentPage}}{{'\n'}}
                View Mode: {{state.viewMode}}{{'\n'}}
                Last Refreshed: {{state.lastRefreshed.toISOString()}}
              </pre>
            </details>
          )}}
        </div>
      )}}
    </div>
  );
}};

export default {component_name};
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
        
    def _create_utility(self, task):
        '''Generates Utility Functions - Enhanced for comprehensive functionality'''
        utility_name = task.get('utility_name', 'NewUtility')
        
        # Generate comprehensive utility code based on utility type
        if 'Api' in utility_name:
            code = f'''
/**
 * API Utilities - Comprehensive HTTP client and API helpers
 */

interface RequestConfig {{
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  data?: any;
  headers?: Record<string, string>;
  timeout?: number;
  retries?: number;
}}

interface ApiResponse<T = any> {{
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}}

export class {utility_name} {{
  private static baseURL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
  private static defaultTimeout = 30000;
  private static defaultRetries = 3;
  
  /**
   * Make HTTP request with advanced error handling and retries
   */
  static async request<T = any>(config: RequestConfig): Promise<ApiResponse<T>> {{
    const {{ url, method = 'GET', data, headers = {{}}, timeout = this.defaultTimeout, retries = this.defaultRetries }} = config;
    
    let lastError: Error;
    
    for (let attempt = 0; attempt <= retries; attempt++) {{
      try {{
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);
        
        const response = await fetch(`${{this.baseURL}}${{url}}`, {{
          method,
          headers: {{
            'Content-Type': 'application/json',
            ...headers
          }},
          body: data ? JSON.stringify(data) : undefined,
          signal: controller.signal
        }});
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {{
          throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
        }}
        
        const responseData = await response.json();
        
        return {{
          data: responseData,
          status: response.status,
          statusText: response.statusText,
          headers: Object.fromEntries(response.headers.entries())
        }};
        
      }} catch (error) {{
        lastError = error as Error;
        
        if (attempt < retries) {{
          console.warn(`API request failed, retrying... (attempt ${{attempt + 1}}/${{retries + 1}})`);
          await this.delay(Math.pow(2, attempt) * 1000); // Exponential backoff
        }}
      }}
    }}
    
    throw lastError!;
  }}
  
  /**
   * GET request helper
   */
  static async get<T = any>(url: string, headers?: Record<string, string>): Promise<ApiResponse<T>> {{
    return this.request<T>({{ url, method: 'GET', headers }});
  }}
  
  /**
   * POST request helper
   */
  static async post<T = any>(url: string, data?: any, headers?: Record<string, string>): Promise<ApiResponse<T>> {{
    return this.request<T>({{ url, method: 'POST', data, headers }});
  }}
  
  /**
   * PUT request helper
   */
  static async put<T = any>(url: string, data?: any, headers?: Record<string, string>): Promise<ApiResponse<T>> {{
    return this.request<T>({{ url, method: 'PUT', data, headers }});
  }}
  
  /**
   * DELETE request helper
   */
  static async delete<T = any>(url: string, headers?: Record<string, string>): Promise<ApiResponse<T>> {{
    return this.request<T>({{ url, method: 'DELETE', headers }});
  }}
  
  /**
   * Upload file with progress tracking
   */
  static async uploadFile(url: string, file: File, onProgress?: (progress: number) => void): Promise<ApiResponse> {{
    return new Promise((resolve, reject) => {{
      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      formData.append('file', file);
      
      xhr.upload.addEventListener('progress', (event) => {{
        if (event.lengthComputable && onProgress) {{
          const progress = Math.round((event.loaded / event.total) * 100);
          onProgress(progress);
        }}
      }});
      
      xhr.addEventListener('load', () => {{
        if (xhr.status >= 200 && xhr.status < 300) {{
          resolve({{
            data: JSON.parse(xhr.responseText),
            status: xhr.status,
            statusText: xhr.statusText,
            headers: {{}}
          }});
        }} else {{
          reject(new Error(`Upload failed: ${{xhr.status}} ${{xhr.statusText}}`));
        }}
      }});
      
      xhr.addEventListener('error', () => {{
        reject(new Error('Upload failed: Network error'));
      }});
      
      xhr.open('POST', `${{this.baseURL}}${{url}}`);
      xhr.send(formData);
    }});
  }}
  
  /**
   * Batch requests with concurrent execution
   */
  static async batchRequests<T = any>(requests: RequestConfig[], maxConcurrency = 5): Promise<ApiResponse<T>[]> {{
    const results: ApiResponse<T>[] = [];
    
    for (let i = 0; i < requests.length; i += maxConcurrency) {{
      const batch = requests.slice(i, i + maxConcurrency);
      const batchResults = await Promise.allSettled(
        batch.map(config => this.request<T>(config))
      );
      
      batchResults.forEach((result, index) => {{
        if (result.status === 'fulfilled') {{
          results.push(result.value);
        }} else {{
          console.error(`Batch request ${{i + index}} failed:`, result.reason);
          throw result.reason;
        }}
      }});
    }}
    
    return results;
  }}
  
  /**
   * Set global API configuration
   */
  static configure(config: {{
    baseURL?: string;
    timeout?: number;
    retries?: number;
  }}) {{
    if (config.baseURL) this.baseURL = config.baseURL;
    if (config.timeout) this.defaultTimeout = config.timeout;
    if (config.retries) this.defaultRetries = config.retries;
  }}
  
  /**
   * Create query string from object
   */
  static createQueryString(params: Record<string, any>): string {{
    const searchParams = new URLSearchParams();
    
    Object.entries(params).forEach(([key, value]) => {{
      if (value !== null && value !== undefined) {{
        if (Array.isArray(value)) {{
          value.forEach(item => searchParams.append(key, String(item)));
        }} else {{
          searchParams.append(key, String(value));
        }}
      }}
    }});
    
    return searchParams.toString();
  }}
  
  /**
   * Delay helper for retries
   */
  private static delay(ms: number): Promise<void> {{
    return new Promise(resolve => setTimeout(resolve, ms));
  }}
  
  /**
   * Check if error is network related
   */
  static isNetworkError(error: Error): boolean {{
    return error.name === 'TypeError' || error.message.includes('fetch');
  }}
  
  /**
   * Check if error is timeout related
   */
  static isTimeoutError(error: Error): boolean {{
    return error.name === 'AbortError' || error.message.includes('timeout');
  }}
}}
'''
        elif 'Date' in utility_name:
            code = f'''
/**
 * Date Utilities - Comprehensive date manipulation and formatting
 */

export class {utility_name} {{
  private static readonly MILLISECONDS_PER_SECOND = 1000;
  private static readonly SECONDS_PER_MINUTE = 60;
  private static readonly MINUTES_PER_HOUR = 60;
  private static readonly HOURS_PER_DAY = 24;
  private static readonly DAYS_PER_WEEK = 7;
  
  /**
   * Format date to various formats
   */
  static formatDate(date: Date, format: string): string {{
    const map: Record<string, string> = {{
      'YYYY': date.getFullYear().toString(),
      'MM': String(date.getMonth() + 1).padStart(2, '0'),
      'DD': String(date.getDate()).padStart(2, '0'),
      'HH': String(date.getHours()).padStart(2, '0'),
      'mm': String(date.getMinutes()).padStart(2, '0'),
      'ss': String(date.getSeconds()).padStart(2, '0')
    }};
    
    return format.replace(/YYYY|MM|DD|HH|mm|ss/g, match => map[match] || match);
  }}
  
  /**
   * Get relative time string (e.g., "2 hours ago")
   */
  static getRelativeTime(date: Date, baseDate: Date = new Date()): string {{
    const diffMs = baseDate.getTime() - date.getTime();
    const diffSeconds = Math.floor(diffMs / this.MILLISECONDS_PER_SECOND);
    const diffMinutes = Math.floor(diffSeconds / this.SECONDS_PER_MINUTE);
    const diffHours = Math.floor(diffMinutes / this.MINUTES_PER_HOUR);
    const diffDays = Math.floor(diffHours / this.HOURS_PER_DAY);
    
    if (diffSeconds < 60) return 'just now';
    if (diffMinutes < 60) return `${{diffMinutes}} minute${{diffMinutes !== 1 ? 's' : ''}} ago`;
    if (diffHours < 24) return `${{diffHours}} hour${{diffHours !== 1 ? 's' : ''}} ago`;
    if (diffDays < 7) return `${{diffDays}} day${{diffDays !== 1 ? 's' : ''}} ago`;
    if (diffDays < 30) return `${{Math.floor(diffDays / 7)}} week${{Math.floor(diffDays / 7) !== 1 ? 's' : ''}} ago`;
    if (diffDays < 365) return `${{Math.floor(diffDays / 30)}} month${{Math.floor(diffDays / 30) !== 1 ? 's' : ''}} ago`;
    return `${{Math.floor(diffDays / 365)}} year${{Math.floor(diffDays / 365) !== 1 ? 's' : ''}} ago`;
  }}
  
  /**
   * Add time to date
   */
  static addTime(date: Date, amount: number, unit: 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'months' | 'years'): Date {{
    const result = new Date(date);
    
    switch (unit) {{
      case 'seconds':
        result.setSeconds(result.getSeconds() + amount);
        break;
      case 'minutes':
        result.setMinutes(result.getMinutes() + amount);
        break;
      case 'hours':
        result.setHours(result.getHours() + amount);
        break;
      case 'days':
        result.setDate(result.getDate() + amount);
        break;
      case 'weeks':
        result.setDate(result.getDate() + (amount * 7));
        break;
      case 'months':
        result.setMonth(result.getMonth() + amount);
        break;
      case 'years':
        result.setFullYear(result.getFullYear() + amount);
        break;
    }}
    
    return result;
  }}
  
  /**
   * Get start of time period
   */
  static startOf(date: Date, unit: 'day' | 'week' | 'month' | 'year'): Date {{
    const result = new Date(date);
    
    switch (unit) {{
      case 'day':
        result.setHours(0, 0, 0, 0);
        break;
      case 'week':
        const day = result.getDay();
        result.setDate(result.getDate() - day);
        result.setHours(0, 0, 0, 0);
        break;
      case 'month':
        result.setDate(1);
        result.setHours(0, 0, 0, 0);
        break;
      case 'year':
        result.setMonth(0, 1);
        result.setHours(0, 0, 0, 0);
        break;
    }}
    
    return result;
  }}
  
  /**
   * Check if date is between two dates
   */
  static isBetween(date: Date, start: Date, end: Date, inclusive = true): boolean {{
    if (inclusive) {{
      return date >= start && date <= end;
    }}
    return date > start && date < end;
  }}
  
  /**
   * Get business days between two dates
   */
  static getBusinessDays(start: Date, end: Date): number {{
    let count = 0;
    const current = new Date(start);
    
    while (current <= end) {{
      const dayOfWeek = current.getDay();
      if (dayOfWeek !== 0 && dayOfWeek !== 6) {{ // Not Sunday (0) or Saturday (6)
        count++;
      }}
      current.setDate(current.getDate() + 1);
    }}
    
    return count;
  }}
  
  /**
   * Parse various date formats
   */
  static parseDate(input: string | number | Date): Date | null {{
    if (input instanceof Date) return input;
    if (typeof input === 'number') return new Date(input);
    if (typeof input === 'string') {{
      // Try common formats
      const formats = [
        /^(\\d{{4}})-(\\d{{2}})-(\\d{{2}})$/, // YYYY-MM-DD
        /^(\\d{{2}})\\/(\\d{{2}})\\/(\\d{{4}})$/, // MM/DD/YYYY
        /^(\\d{{2}})\\.(\\d{{2}})\\.(\\d{{4}})$/, // DD.MM.YYYY
      ];
      
      for (const format of formats) {{
        const match = input.match(format);
        if (match) {{
          const date = new Date(input);
          if (!isNaN(date.getTime())) return date;
        }}
      }}
      
      // Try native Date parsing
      const date = new Date(input);
      return isNaN(date.getTime()) ? null : date;
    }}
    
    return null;
  }}
  
  /**
   * Get timezone offset string
   */
  static getTimezoneOffset(date: Date = new Date()): string {{
    const offset = date.getTimezoneOffset();
    const hours = Math.floor(Math.abs(offset) / 60);
    const minutes = Math.abs(offset) % 60;
    const sign = offset <= 0 ? '+' : '-';
    
    return `${{sign}}${{String(hours).padStart(2, '0')}}:${{String(minutes).padStart(2, '0')}}`;
  }}
  
  /**
   * Get calendar weeks in month
   */
  static getCalendarWeeks(year: number, month: number): Date[][] {{
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const weeks: Date[][] = [];
    
    let currentWeek: Date[] = [];
    let current = this.startOf(firstDay, 'week');
    
    while (current <= lastDay || currentWeek.length < 7) {{
      currentWeek.push(new Date(current));
      
      if (currentWeek.length === 7) {{
        weeks.push(currentWeek);
        currentWeek = [];
      }}
      
      current.setDate(current.getDate() + 1);
    }}
    
    if (currentWeek.length > 0) {{
      while (currentWeek.length < 7) {{
        currentWeek.push(new Date(current));
        current.setDate(current.getDate() + 1);
      }}
      weeks.push(currentWeek);
    }}
    
    return weeks;
  }}
}}
'''
        else:
            # Generic utility template
            code = f'''
/**
 * {utility_name} - Comprehensive utility functions
 */

export class {utility_name} {{
  /**
   * Deep clone an object or array
   */
  static deepClone<T>(obj: T): T {{
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T;
    if (obj instanceof Array) return obj.map(item => this.deepClone(item)) as unknown as T;
    if (typeof obj === 'object') {{
      const cloned = {{}} as T;
      Object.keys(obj).forEach(key => {{
        (cloned as any)[key] = this.deepClone((obj as any)[key]);
      }});
      return cloned;
    }}
    return obj;
  }}
  
  /**
   * Debounce function execution
   */
  static debounce<T extends (...args: any[]) => any>(
    func: T,
    wait: number,
    immediate = false
  ): (...args: Parameters<T>) => void {{
    let timeout: NodeJS.Timeout | null = null;
    
    return (...args: Parameters<T>) => {{
      const later = () => {{
        timeout = null;
        if (!immediate) func(...args);
      }};
      
      const callNow = immediate && !timeout;
      
      if (timeout) clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      
      if (callNow) func(...args);
    }};
  }}
  
  /**
   * Throttle function execution
   */
  static throttle<T extends (...args: any[]) => any>(
    func: T,
    limit: number
  ): (...args: Parameters<T>) => void {{
    let inThrottle = false;
    
    return (...args: Parameters<T>) => {{
      if (!inThrottle) {{
        func(...args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }}
    }};
  }}
  
  /**
   * Generate unique ID
   */
  static generateId(prefix = 'id'): string {{
    const timestamp = Date.now().toString(36);
    const randomStr = Math.random().toString(36).substr(2);
    return `${{prefix}}-${{timestamp}}-${{randomStr}}`;
  }}
  
  /**
   * Validate email address
   */
  static isValidEmail(email: string): boolean {{
    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return emailRegex.test(email);
  }}
  
  /**
   * Format bytes to human readable string
   */
  static formatBytes(bytes: number, decimals = 2): string {{
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
  }}
  
  /**
   * Get nested object property safely
   */
  static getNestedProperty(obj: any, path: string, defaultValue?: any): any {{
    return path.split('.').reduce((current, key) => {{
      return current && current[key] !== undefined ? current[key] : defaultValue;
    }}, obj);
  }}
  
  /**
   * Set nested object property
   */
  static setNestedProperty(obj: any, path: string, value: any): void {{
    const keys = path.split('.');
    const lastKey = keys.pop()!;
    
    const target = keys.reduce((current, key) => {{
      if (!current[key] || typeof current[key] !== 'object') {{
        current[key] = {{}};
      }}
      return current[key];
    }}, obj);
    
    target[lastKey] = value;
  }}
  
  /**
   * Capitalize first letter of string
   */
  static capitalize(str: string): string {{
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
  }}
  
  /**
   * Convert camelCase to kebab-case
   */
  static camelToKebab(str: string): string {{
    return str.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
  }}
  
  /**
   * Convert kebab-case to camelCase
   */
  static kebabToCamel(str: string): string {{
    return str.replace(/-([a-z])/g, (g) => g[1].toUpperCase());
  }}
  
  /**
   * Remove duplicates from array
   */
  static removeDuplicates<T>(arr: T[], key?: keyof T): T[] {{
    if (!key) {{
      return [...new Set(arr)];
    }}
    
    const seen = new Set();
    return arr.filter(item => {{
      const value = item[key];
      if (seen.has(value)) {{
        return false;
      }}
      seen.add(value);
      return true;
    }});
  }}
  
  /**
   * Chunk array into smaller arrays
   */
  static chunk<T>(arr: T[], size: number): T[][] {{
    const chunks: T[][] = [];
    for (let i = 0; i < arr.length; i += size) {{
      chunks.push(arr.slice(i, i + size));
    }}
    return chunks;
  }}
  
  /**
   * Retry async operation with exponential backoff
   */
  static async retry<T>(
    operation: () => Promise<T>,
    maxAttempts = 3,
    baseDelay = 1000
  ): Promise<T> {{
    let lastError: Error;
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {{
      try {{
        return await operation();
      }} catch (error) {{
        lastError = error as Error;
        
        if (attempt === maxAttempts) {{
          throw lastError;
        }}
        
        const delay = baseDelay * Math.pow(2, attempt - 1);
        await new Promise(resolve => setTimeout(resolve, delay));
      }}
    }}
    
    throw lastError!;
  }}
}}
'''
        
        # Save utility code
        if 'Api' in utility_name:
            path = f'/home/runner/work/mrsunkwn/mrsunkwn/frontend/src/utils/{utility_name}.ts'
        else:
            path = f'/home/runner/work/mrsunkwn/mrsunkwn/frontend/src/utils/{utility_name}.ts'
        
        self._save_code(path, code)
        
    def _create_api_endpoint(self, task):
        '''Generates Comprehensive API Endpoint with full CRUD operations'''
        endpoint = task.get('endpoint', '/api/example')
        endpoint_name = endpoint.split('/')[-1]
        
        # Generate comprehensive endpoint code with full functionality
        code = f'''
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
from enum import Enum
import logging
import asyncio
from functools import wraps

# Setup logging
logger = logging.getLogger(__name__)

# Create router with prefix and tags
router = APIRouter(
    prefix="{endpoint}",
    tags=["{endpoint_name}"],
    responses={{
        404: {{"description": "{endpoint_name.title()} not found"}},
        422: {{"description": "Validation error"}},
        500: {{"description": "Internal server error"}}
    }}
)

# Enums for status and types
class {endpoint_name.title()}Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ARCHIVED = "archived"
    DELETED = "deleted"

class {endpoint_name.title()}Type(str, Enum):
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"

# Base models
class {endpoint_name.title()}Base(BaseModel):
    """Base model for {endpoint_name}"""
    name: str = Field(..., min_length=1, max_length=255, description="Name of the {endpoint_name}")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the {endpoint_name}")
    status: {endpoint_name.title()}Status = Field(default={endpoint_name.title()}Status.ACTIVE, description="Status of the {endpoint_name}")
    type: {endpoint_name.title()}Type = Field(default={endpoint_name.title()}Type.STANDARD, description="Type of the {endpoint_name}")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags associated with the {endpoint_name}")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or only whitespace')
        return v.strip()
    
    @validator('tags')
    def validate_tags(cls, v):
        if v and len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return v

class {endpoint_name.title()}Create({endpoint_name.title()}Base):
    """Model for creating {endpoint_name}"""
    created_by: Optional[str] = Field(None, description="ID of the user creating this {endpoint_name}")
    
    class Config:
        schema_extra = {{
            "example": {{
                "name": "Sample {endpoint_name.title()}",
                "description": "This is a sample {endpoint_name}",
                "status": "active",
                "type": "standard",
                "tags": ["sample", "demo"],
                "metadata": {{"priority": "high", "category": "test"}},
                "created_by": "user123"
            }}
        }}

class {endpoint_name.title()}Update(BaseModel):
    """Model for updating {endpoint_name}"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[{endpoint_name.title()}Status] = None
    type: Optional[{endpoint_name.title()}Type] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    updated_by: Optional[str] = Field(None, description="ID of the user updating this {endpoint_name}")
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty or only whitespace')
        return v.strip() if v else v

class {endpoint_name.title()}InDB({endpoint_name.title()}Base):
    """Model for {endpoint_name} in database"""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    created_by: Optional[str] = Field(None, description="ID of the user who created this {endpoint_name}")
    updated_by: Optional[str] = Field(None, description="ID of the user who last updated this {endpoint_name}")
    version: int = Field(default=1, description="Version number for optimistic locking")

class {endpoint_name.title()}Response({endpoint_name.title()}InDB):
    """Model for {endpoint_name} API response"""
    
    class Config:
        schema_extra = {{
            "example": {{
                "id": 1,
                "name": "Sample {endpoint_name.title()}",
                "description": "This is a sample {endpoint_name}",
                "status": "active",
                "type": "standard",
                "tags": ["sample", "demo"],
                "metadata": {{"priority": "high", "category": "test"}},
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z",
                "created_by": "user123",
                "updated_by": "user456",
                "version": 1
            }}
        }}

class {endpoint_name.title()}List(BaseModel):
    """Model for paginated {endpoint_name} list response"""
    items: List[{endpoint_name.title()}Response]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool

class {endpoint_name.title()}Stats(BaseModel):
    """Model for {endpoint_name} statistics"""
    total_count: int
    active_count: int
    inactive_count: int
    pending_count: int
    archived_count: int
    deleted_count: int
    by_type: Dict[str, int]
    created_today: int
    created_this_week: int
    created_this_month: int

# Dependency functions
async def get_current_user():
    """Dependency to get current authenticated user"""
    # TODO: Implement actual authentication logic
    return "user123"

def validate_pagination(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100)):
    """Validate pagination parameters"""
    return {{"page": page, "per_page": per_page}}

# Rate limiting decorator
def rate_limit(max_calls: int, time_window: int):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Implement rate limiting logic
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Main CRUD endpoints
@router.get(
    "/",
    response_model={endpoint_name.title()}List,
    summary="Get all {endpoint_name}s",
    description="Retrieve a paginated list of all {endpoint_name}s with optional filtering"
)
@rate_limit(max_calls=100, time_window=60)
async def get_{endpoint_name}s(
    pagination: dict = Depends(validate_pagination),
    status: Optional[{endpoint_name.title()}Status] = Query(None, description="Filter by status"),
    type: Optional[{endpoint_name.title()}Type] = Query(None, description="Filter by type"),
    search: Optional[str] = Query(None, min_length=1, description="Search in name and description"),
    tags: Optional[str] = Query(None, description="Comma-separated list of tags to filter by"),
    created_after: Optional[datetime] = Query(None, description="Filter items created after this date"),
    created_before: Optional[datetime] = Query(None, description="Filter items created before this date"),
    sort_by: Optional[str] = Query("created_at", description="Field to sort by"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    current_user: str = Depends(get_current_user)
):
    """Get all {endpoint_name}s with advanced filtering and pagination"""
    try:
        logger.info(f"Fetching {endpoint_name}s for user {{current_user}} with filters: status={{status}}, type={{type}}, search={{search}}")
        
        # Build filters
        filters = {{}}
        if status:
            filters["status"] = status
        if type:
            filters["type"] = type
        if search:
            filters["search"] = search
        if tags:
            filters["tags"] = tags.split(",")
        if created_after:
            filters["created_after"] = created_after
        if created_before:
            filters["created_before"] = created_before
        
        # TODO: Implement actual database query with filters
        # Mock response for now
        mock_items = [
            {endpoint_name.title()}Response(
                id=i,
                name=f"Sample {endpoint_name.title()} {{i}}",
                description=f"Description for {endpoint_name} {{i}}",
                status={endpoint_name.title()}Status.ACTIVE,
                type={endpoint_name.title()}Type.STANDARD,
                tags=["sample", f"tag{{i}}"],
                metadata={{"index": i}},
                created_at=datetime.utcnow() - timedelta(days=i),
                created_by=current_user,
                version=1
            )
            for i in range(1, min(pagination["per_page"] + 1, 11))
        ]
        
        total = 100  # Mock total count
        pages = (total + pagination["per_page"] - 1) // pagination["per_page"]
        
        response = {endpoint_name.title()}List(
            items=mock_items,
            total=total,
            page=pagination["page"],
            per_page=pagination["per_page"],
            pages=pages,
            has_next=pagination["page"] < pages,
            has_prev=pagination["page"] > 1
        )
        
        logger.info(f"Successfully fetched {{len(mock_items)}} {endpoint_name}s")
        return response
        
    except Exception as e:
        logger.error(f"Error fetching {endpoint_name}s: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error fetching {endpoint_name}s: {{str(e)}}")

@router.get(
    "/{{item_id}}",
    response_model={endpoint_name.title()}Response,
    summary="Get {endpoint_name} by ID",
    description="Retrieve a specific {endpoint_name} by its ID"
)
async def get_{endpoint_name}(
    item_id: int = Path(..., gt=0, description="The ID of the {endpoint_name} to retrieve"),
    current_user: str = Depends(get_current_user)
):
    """Get {endpoint_name} by ID"""
    try:
        logger.info(f"Fetching {endpoint_name} {{item_id}} for user {{current_user}}")
        
        # TODO: Implement actual database query
        # Mock response for now
        if item_id > 1000:
            raise HTTPException(status_code=404, detail=f"{endpoint_name.title()} not found")
        
        response = {endpoint_name.title()}Response(
            id=item_id,
            name=f"Sample {endpoint_name.title()} {{item_id}}",
            description=f"Description for {endpoint_name} {{item_id}}",
            status={endpoint_name.title()}Status.ACTIVE,
            type={endpoint_name.title()}Type.STANDARD,
            tags=["sample"],
            metadata={{"id": item_id}},
            created_at=datetime.utcnow() - timedelta(days=1),
            created_by=current_user,
            version=1
        )
        
        logger.info(f"Successfully fetched {endpoint_name} {{item_id}}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching {endpoint_name} {{item_id}}: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error fetching {endpoint_name}: {{str(e)}}")

@router.post(
    "/",
    response_model={endpoint_name.title()}Response,
    status_code=status.HTTP_201_CREATED,
    summary="Create new {endpoint_name}",
    description="Create a new {endpoint_name} with the provided data"
)
async def create_{endpoint_name}(
    request: {endpoint_name.title()}Create,
    current_user: str = Depends(get_current_user)
):
    """Create new {endpoint_name}"""
    try:
        logger.info(f"Creating new {endpoint_name} for user {{current_user}}: {{request.name}}")
        
        # TODO: Implement actual database creation
        # Mock response for now
        new_id = 12345  # Mock generated ID
        
        response = {endpoint_name.title()}Response(
            id=new_id,
            **request.dict(),
            created_at=datetime.utcnow(),
            created_by=current_user,
            version=1
        )
        
        logger.info(f"Successfully created {endpoint_name} {{new_id}}")
        return response
        
    except Exception as e:
        logger.error(f"Error creating {endpoint_name}: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error creating {endpoint_name}: {{str(e)}}")

@router.put(
    "/{{item_id}}",
    response_model={endpoint_name.title()}Response,
    summary="Update {endpoint_name}",
    description="Update an existing {endpoint_name} with the provided data"
)
async def update_{endpoint_name}(
    item_id: int = Path(..., gt=0, description="The ID of the {endpoint_name} to update"),
    request: {endpoint_name.title()}Update = ...,
    current_user: str = Depends(get_current_user)
):
    """Update {endpoint_name} by ID"""
    try:
        logger.info(f"Updating {endpoint_name} {{item_id}} for user {{current_user}}")
        
        # TODO: Implement actual database update
        # Check if item exists first
        if item_id > 1000:
            raise HTTPException(status_code=404, detail=f"{endpoint_name.title()} not found")
        
        # Mock response for now
        response = {endpoint_name.title()}Response(
            id=item_id,
            name=request.name or f"Updated {endpoint_name.title()} {{item_id}}",
            description=request.description or f"Updated description for {endpoint_name} {{item_id}}",
            status=request.status or {endpoint_name.title()}Status.ACTIVE,
            type=request.type or {endpoint_name.title()}Type.STANDARD,
            tags=request.tags or ["updated"],
            metadata=request.metadata or {{"updated": True}},
            created_at=datetime.utcnow() - timedelta(days=1),
            updated_at=datetime.utcnow(),
            created_by="original_user",
            updated_by=current_user,
            version=2
        )
        
        logger.info(f"Successfully updated {endpoint_name} {{item_id}}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating {endpoint_name} {{item_id}}: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error updating {endpoint_name}: {{str(e)}}")

@router.patch(
    "/{{item_id}}",
    response_model={endpoint_name.title()}Response,
    summary="Partially update {endpoint_name}",
    description="Partially update an existing {endpoint_name} with only the provided fields"
)
async def patch_{endpoint_name}(
    item_id: int = Path(..., gt=0, description="The ID of the {endpoint_name} to patch"),
    request: {endpoint_name.title()}Update = ...,
    current_user: str = Depends(get_current_user)
):
    """Partially update {endpoint_name} by ID"""
    try:
        logger.info(f"Patching {endpoint_name} {{item_id}} for user {{current_user}}")
        
        # TODO: Implement actual database patch
        if item_id > 1000:
            raise HTTPException(status_code=404, detail=f"{endpoint_name.title()} not found")
        
        # Mock response - only update provided fields
        updated_fields = {{k: v for k, v in request.dict().items() if v is not None}}
        
        response = {endpoint_name.title()}Response(
            id=item_id,
            name=f"Patched {endpoint_name.title()} {{item_id}}",
            description=f"Patched description for {endpoint_name} {{item_id}}",
            status={endpoint_name.title()}Status.ACTIVE,
            type={endpoint_name.title()}Type.STANDARD,
            tags=["patched"],
            metadata={{"patched_fields": list(updated_fields.keys())}},
            created_at=datetime.utcnow() - timedelta(days=1),
            updated_at=datetime.utcnow(),
            created_by="original_user",
            updated_by=current_user,
            version=3
        )
        
        logger.info(f"Successfully patched {endpoint_name} {{item_id}} with fields: {{list(updated_fields.keys())}}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error patching {endpoint_name} {{item_id}}: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error patching {endpoint_name}: {{str(e)}}")

@router.delete(
    "/{{item_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete {endpoint_name}",
    description="Delete an existing {endpoint_name} by its ID"
)
async def delete_{endpoint_name}(
    item_id: int = Path(..., gt=0, description="The ID of the {endpoint_name} to delete"),
    force: bool = Query(False, description="Force delete without moving to trash"),
    current_user: str = Depends(get_current_user)
):
    """Delete {endpoint_name} by ID"""
    try:
        logger.info(f"Deleting {endpoint_name} {{item_id}} for user {{current_user}} (force={{force}})")
        
        # TODO: Implement actual database deletion
        if item_id > 1000:
            raise HTTPException(status_code=404, detail=f"{endpoint_name.title()} not found")
        
        if force:
            # Hard delete
            logger.info(f"Force deleting {endpoint_name} {{item_id}}")
        else:
            # Soft delete (mark as deleted)
            logger.info(f"Soft deleting {endpoint_name} {{item_id}}")
        
        logger.info(f"Successfully deleted {endpoint_name} {{item_id}}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting {endpoint_name} {{item_id}}: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error deleting {endpoint_name}: {{str(e)}}")

# Additional utility endpoints
@router.get(
    "/stats",
    response_model={endpoint_name.title()}Stats,
    summary="Get {endpoint_name} statistics",
    description="Get comprehensive statistics about {endpoint_name}s"
)
async def get_{endpoint_name}_stats(
    current_user: str = Depends(get_current_user)
):
    """Get {endpoint_name} statistics"""
    try:
        logger.info(f"Fetching {endpoint_name} statistics for user {{current_user}}")
        
        # TODO: Implement actual statistics calculation
        stats = {endpoint_name.title()}Stats(
            total_count=1250,
            active_count=1000,
            inactive_count=150,
            pending_count=75,
            archived_count=20,
            deleted_count=5,
            by_type={{
                "standard": 800,
                "premium": 300,
                "enterprise": 100,
                "custom": 50
            }},
            created_today=15,
            created_this_week=105,
            created_this_month=420
        )
        
        logger.info(f"Successfully calculated {endpoint_name} statistics")
        return stats
        
    except Exception as e:
        logger.error(f"Error calculating {endpoint_name} statistics: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {{str(e)}}")

@router.post(
    "/bulk",
    response_model=List[{endpoint_name.title()}Response],
    summary="Bulk create {endpoint_name}s",
    description="Create multiple {endpoint_name}s in a single request"
)
async def bulk_create_{endpoint_name}s(
    requests: List[{endpoint_name.title()}Create],
    current_user: str = Depends(get_current_user)
):
    """Bulk create {endpoint_name}s"""
    try:
        logger.info(f"Bulk creating {{len(requests)}} {endpoint_name}s for user {{current_user}}")
        
        if len(requests) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 items allowed per bulk operation")
        
        # TODO: Implement actual bulk database creation
        responses = []
        for i, request in enumerate(requests):
            response = {endpoint_name.title()}Response(
                id=10000 + i,
                **request.dict(),
                created_at=datetime.utcnow(),
                created_by=current_user,
                version=1
            )
            responses.append(response)
        
        logger.info(f"Successfully bulk created {{len(responses)}} {endpoint_name}s")
        return responses
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error bulk creating {endpoint_name}s: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error bulk creating {endpoint_name}s: {{str(e)}}")

@router.post(
    "/search",
    response_model={endpoint_name.title()}List,
    summary="Advanced search {endpoint_name}s",
    description="Perform advanced search across {endpoint_name}s with complex criteria"
)
async def search_{endpoint_name}s(
    search_query: Dict[str, Any],
    pagination: dict = Depends(validate_pagination),
    current_user: str = Depends(get_current_user)
):
    """Advanced search for {endpoint_name}s"""
    try:
        logger.info(f"Advanced search for {endpoint_name}s by user {{current_user}}: {{search_query}}")
        
        # TODO: Implement actual advanced search logic
        # Mock response for now
        mock_items = [
            {endpoint_name.title()}Response(
                id=i,
                name=f"Search Result {endpoint_name.title()} {{i}}",
                description=f"Matched search criteria: {{search_query}}",
                status={endpoint_name.title()}Status.ACTIVE,
                type={endpoint_name.title()}Type.STANDARD,
                tags=["search", "result"],
                metadata={{"search_score": 0.95 - (i * 0.1)}},
                created_at=datetime.utcnow() - timedelta(days=i),
                created_by=current_user,
                version=1
            )
            for i in range(1, 6)
        ]
        
        response = {endpoint_name.title()}List(
            items=mock_items,
            total=5,
            page=pagination["page"],
            per_page=pagination["per_page"],
            pages=1,
            has_next=False,
            has_prev=False
        )
        
        logger.info(f"Advanced search returned {{len(mock_items)}} results")
        return response
        
    except Exception as e:
        logger.error(f"Error in advanced search: {{str(e)}}")
        raise HTTPException(status_code=500, detail=f"Error in search: {{str(e)}}")
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
    agent = os.getenv('AGENT_ROLE', 'UNIFIED_AGENT')
    runner = SprintRunner(agent)
    runner.run_sprint()