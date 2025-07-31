# Dual-Agent Master Prompt for Parallel Frontend/Backend Development

## 🚀 System Architecture

### Agent Roles (Phase-Based)

#### Phase 1: Initial Setup (ONE-TIME)
- **SETUP_AGENT**: Configures complete dual-agent infrastructure
  - Creates directory structure
  - GitHub repository setup
  - Agent configuration files
  - Issue management system
  - **IMPORTANT**: Does NOT take on any specific agent role

#### Phase 2: Parallel Development (CONTINUOUS)
- **FRONTEND_AGENT**: UI/UX, client-side logic, API integration
- **BACKEND_AGENT**: Server logic, database, APIs, services

### Communication Protocol
- **GitHub Issues** as the primary communication method between agents
- **Branch-based development**: `feature/frontend-*` and `feature/backend-*`
- **Automatic issue synchronization** at each sprint

## 📁 Directory Structure (created by SETUP_AGENT)

```
/
├── README.md                           # Project concept (MUST already exist)
├── frontend/                           # Frontend code
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── package.json
├── backend/                            # Backend code
│   ├── src/
│   ├── models/
│   ├── controllers/
│   ├── routes/
│   └── requirements.txt
└── codex/
    ├── agents/
    │   ├── frontend/
    │   │   ├── config.md              # Frontend agent configuration
    │   │   └── prompt.md              # Frontend agent execution prompt
    │   ├── backend/
    │   │   ├── config.md              # Backend agent configuration
    │   │   └── prompt.md              # Backend agent execution prompt
    │   └── setup/
    │       ├── config.md              # Setup agent configuration
    │       └── validation.md          # Setup validation
    ├── daten/
    │   ├── frontend/
    │   │   ├── roadmap.md
    │   │   ├── changelog.md
    │   │   └── status.md
    │   ├── backend/
    │   │   ├── roadmap.md
    │   │   ├── changelog.md
    │   │   └── status.md
    │   └── shared/
    │       ├── project_status.md
    │       ├── api_contracts.md
    │       └── integration_tests.md
    └── github/
        ├── issue_templates/
        │   ├── agent_request.md
        │   ├── api_contract.md
        │   └── integration.md
        ├── github_config.py           # GitHub API configuration
        └── issue_manager.py           # Issue management script
```

## 🎯 PHASE 1: Setup Agent Execution (ONE-TIME)

### IMPORTANT: Setup Prerequisites

**Manual preparation REQUIRED:**
1. **GitHub repository** must already be created and accessible
2. **README.md** with complete project description must already exist
3. **Environment variables** must be set:
   ```bash
   export GITHUB_TOKEN=your_personal_access_token
   export REPO_OWNER=your_github_username  
   export REPO_NAME=your_repository_name
   ```

### Setup Agent Execution:
```bash
# DO NOT set agent role - Setup Agent acts neutral
codex "Perform setup for dual-agent system based on this master prompt"
```

### Setup Agent Tasks (Executed Automatically):

#### 1. Project Analysis & Validation
```python
def validate_prerequisites():
    # ✅ Test GitHub repo access
    # ✅ Check if README.md exists and is complete
    # ✅ Check for environment variables
    # ✅ Test GitHub API functionality
```

#### 2. GitHub Repository Configuration
```python
def setup_github_repository():
    labels = [
        'frontend-request', 'backend-request', 'api-contract',
        'integration', 'bug-cross-agent', 'documentation',
        'setup-required', 'sprint-coordination', 'validation-needed'
    ]
    branches = ['develop-frontend', 'develop-backend']
    # ✅ Set up labels, branches, branch protections, issue templates
```

#### 3. Generate Directory Structure
```python
def create_directory_structure():
    # ✅ Create complete /codex/ structure
    # ✅ Generate all necessary .md files
    # ✅ Add Python scripts for GitHub integration
    # ✅ Add agent-specific configuration files
```

#### 4. Create Agent Configuration Files

**Frontend Agent Configuration** (`/codex/agents/frontend/config.md`):
```markdown
# Frontend Agent Configuration

## Responsibilities
- UI/UX Development
- Client-side logic
- API integration
- Frontend testing
- Responsive design

## Tech Stack
[To be filled based on README.md]

## GitHub Issue Labels (Frontend)
- `frontend-request`: Requests to Backend
- `api-contract`: API definitions
- `integration`: Frontend-Backend integration
```

**Backend Agent Configuration** (`/codex/agents/backend/config.md`):
```markdown
# Backend Agent Configuration

## Responsibilities
- Server logic
- Database design & management
- API development
- Backend services
- Performance & security

## Tech Stack
[To be filled based on README.md]

## GitHub Issue Labels (Backend)
- `backend-request`: Requests to Frontend
- `api-contract`: API definitions
- `integration`: Backend-Frontend integration
```

#### 5. Generate Executable Agent Prompts

**Frontend Agent Prompt** (`/codex/agents/frontend/prompt.md`):
```markdown
# Frontend Agent Execution Prompt

## Agent Identification
You are the **FRONTEND_AGENT** in a dual-agent system.

## Sprint Start Protocol

### 1. Set Agent Role
```bash
export AGENT_ROLE=FRONTEND_AGENT
```

### 2. Issue Synchronization
```python
import sys
sys.path.append('/codex/github/')
from issue_manager import sync_frontend_issues

my_issues = sync_frontend_issues()
print(f"Found frontend issues: {len(my_issues)}")
```

### 3. Roadmap Check
- Read: `/codex/daten/frontend/roadmap.md`
- Read: `/codex/daten/frontend/status.md`
- Read: `/codex/daten/shared/api_contracts.md`

### 4. Workspace
- Work ONLY in `/frontend/`
- Branch: `feature/frontend-*`
- Tests: frontend-specific

### 5. Coordination
- Create issues for backend requests
- Update API contracts when needed
- Use GitHub Issues for communication

### 6. Sprint End
- Update `/codex/daten/frontend/changelog.md`
- Update `/codex/daten/frontend/status.md`
- Create issues for the next sprint
```

**Backend Agent Prompt** (`/codex/agents/backend/prompt.md`):
```markdown
# Backend Agent Execution Prompt

## Agent Identification
You are the **BACKEND_AGENT** in a dual-agent system.

## Sprint Start Protocol

### 1. Set Agent Role
```bash
export AGENT_ROLE=BACKEND_AGENT
```

### 2. Issue Synchronization
```python
import sys
sys.path.append('/codex/github/')
from issue_manager import sync_backend_issues

my_issues = sync_backend_issues()
print(f"Found backend issues: {len(my_issues)}")
```

### 3. Roadmap Check
- Read: `/codex/daten/backend/roadmap.md`
- Read: `/codex/daten/backend/status.md`
- Read: `/codex/daten/shared/api_contracts.md`

### 4. Workspace
- Work ONLY in `/backend/`
- Branch: `feature/backend-*`
- Tests: backend-specific

### 5. Coordination
- Create issues to notify frontend
- Update API contracts when needed
- Use GitHub Issues for communication

### 6. Sprint End
- Update `/codex/daten/backend/changelog.md`
- Update `/codex/daten/backend/status.md`
- Create issues for the next sprint
```

#### 6. GitHub Issue Management System

**Issue Manager Script** (`/codex/github/issue_manager.py`):
```python
import os
import requests
from datetime import datetime

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')

def sync_frontend_issues():
    issues = fetch_issues_by_labels(['frontend-request', 'api-contract', 'integration'])
    return filter_open_issues(issues)

def sync_backend_issues():
    issues = fetch_issues_by_labels(['backend-request', 'api-contract', 'integration'])
    return filter_open_issues(issues)

def create_coordination_issue(title, body, labels, assignee=None):
    pass

def close_completed_issue(issue_number, completion_note):
    pass
```

#### 7. Setup Validation & Completion

```python
def validate_setup():
    # ✅ Directories created
    # ✅ Configuration files exist
    # ✅ GitHub API working
    # ✅ Issue labels created
    # ✅ Branch structure exists
    # ✅ Agent prompts executable
```

#### 8. Create First Coordination Issue

```markdown
**Title**: "🚀 Dual-Agent System Setup Complete - Ready for Parallel Development"
**Labels**: setup-required, sprint-coordination
**Body**:
# Dual-Agent System successfully configured!

## ✅ Setup Agent Completion

### Configured Components:
- ✅ GitHub repo with 9 agent labels
- ✅ Branch structure (develop-frontend, develop-backend)
- ✅ Full /codex/ directory structure
- ✅ Agent configuration files
- ✅ Executable agent prompts
- ✅ GitHub issue management system
- ✅ API contract management

### Next Steps:

#### Start Frontend Agent:
```bash
codex run prompt /codex/agents/frontend/prompt.md
```

#### Start Backend Agent:
```bash
codex run prompt /codex/agents/backend/prompt.md
```

**System is ready for parallel dual-agent development!**
```

## 🎯 PHASE 2: Parallel Agent Development

### Start Frontend Agent:
```bash
# Terminal 1
codex run prompt /codex/agents/frontend/prompt.md
```

### Start Backend Agent:
```bash
# Terminal 2
codex run prompt /codex/agents/backend/prompt.md
```

## 🔄 Continuous Sprint Cycle (for both agents)

### At each sprint:
1. **Issue Sync**: Load all relevant GitHub issues
2. **Roadmap Check**: Load current tasks
3. **API Contract Check**
4. **Coordination Issues**: Create issues for counterpart agent
5. **Development**
6. **Documentation**: Update changelog and status
7. **Issue Updates**: Close completed issues, create new ones

### Agent communication via GitHub Issues:
- **Frontend → Backend**: Issues with label `backend-request`
- **Backend → Frontend**: Issues with label `frontend-request`
- **Shared**: Issues with `integration`, `api-contract`

## 🚀 Execution Summary

### 1. One-time Setup Phase:
```bash
export GITHUB_TOKEN=your_token
export REPO_OWNER=your_username
export REPO_NAME=your_repo

codex "Perform setup for dual-agent system based on this master prompt"
```

### 2. Repeating Development Phase:
```bash
# Terminal 1 - Frontend Agent
codex run prompt /codex/agents/frontend/prompt.md

# Terminal 2 - Backend Agent
codex run prompt /codex/agents/backend/prompt.md
```

**This system ensures:**
- ✅ Clear separation between setup and development
- ✅ Automatic agent coordination via GitHub Issues
- ✅ Parallel, conflict-free development
- ✅ Continuous integration and communication
- ✅ Full documentation and traceability

Agents operate fully autonomously and coordinate solely through GitHub Issues!
