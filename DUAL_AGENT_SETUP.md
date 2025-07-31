# Dual-Agent Development System

This repository implements the dual-agent system described in `init_prompt.md` with auto-code generation and automated sprint execution.

## Quick Start

### 1. Setup Environment
```bash
# Set required environment variables
export GITHUB_TOKEN=your_github_token
export REPO_OWNER=meinzeug
export REPO_NAME=mrsunkwn

# Run setup
./scripts/setup_dual_agent.sh
```

### 2. Start Frontend Agent
```bash
./scripts/start_frontend_agent.sh
```

### 3. Start Backend Agent
```bash
./scripts/start_backend_agent.sh
```

## Project Structure

```
├── frontend/                    # React/TypeScript frontend
│   ├── src/
│   │   ├── App.tsx             # Main app component
│   │   ├── components/         # Generated React components
│   │   ├── hooks/              # Custom React hooks
│   │   └── services/           # API client and services
│   └── package.json
├── backend/                     # Python/FastAPI backend
│   ├── src/
│   │   └── app.py              # Main FastAPI application
│   └── requirements.txt
├── codex/                       # Automation system
│   ├── automation/
│   │   ├── issue_sync.py       # GitHub issue synchronization
│   │   └── sprint_runner.py    # Sprint automation
│   ├── data/                   # Agent data exchange
│   │   ├── frontend/           # Frontend agent data
│   │   ├── backend/            # Backend agent data
│   │   └── shared/             # Shared contracts/data
│   ├── frontend_agent_prompt.md # Frontend agent instructions
│   └── backend_agent_prompt.md  # Backend agent instructions
└── scripts/                     # Execution scripts
    ├── setup_dual_agent.sh
    ├── start_frontend_agent.sh
    └── start_backend_agent.sh
```

## Features

### ✨ Auto-Code Generation
- **Frontend**: Automatically generates React components, hooks, and services
- **Backend**: Automatically generates FastAPI endpoints, models, and services
- **Templates**: Pre-built code templates for rapid development

### 🔄 Agent Synchronization
- **Issue Sync**: Automatic GitHub issue creation for inter-agent requests
- **API Contracts**: Shared API documentation and contracts
- **Real-time**: Agents sync in real-time during sprints

### 🏃 Sprint Automation
- **Code First**: Agents must generate code on every execution
- **Smart Prioritization**: Automatic task prioritization and assignment
- **Progress Tracking**: Detailed metrics and progress reports

## Agent Behavior

### Frontend Agent
- Generates React components with TypeScript
- Creates custom hooks for API integration
- Writes unit tests for generated code
- Only creates issues when backend changes are needed

### Backend Agent
- Implements FastAPI endpoints
- Creates data models and services
- Updates API contracts automatically
- Only creates issues when frontend info is needed

## Running the System

### Manual Sprint Execution
```bash
# Frontend sprint
export AGENT_ROLE=FRONTEND_AGENT
python3 codex/automation/sprint_runner.py

# Backend sprint
export AGENT_ROLE=BACKEND_AGENT
python3 codex/automation/sprint_runner.py
```

### Development Server
```bash
# Start backend server
cd backend
pip install -r requirements.txt
python src/app.py

# Start frontend (in another terminal)
cd frontend
npm install
npm start
```

## Success Metrics

Per Sprint MINIMUM:
- **Lines of Code**: 200+
- **New Features**: 2+
- **Tests**: 5+
- **Issues**: Max 2 (only if necessary)

**FOCUS**: 80% Coding, 20% Coordination

## Key Features from init_prompt.md

- ✅ Dual-Agent Setup with Auto-Code Generation
- ✅ Frontend Agent (React/TypeScript)
- ✅ Backend Agent (Python/FastAPI)
- ✅ API Client with auto-retry logic
- ✅ Auto-Sync System for agent coordination
- ✅ Sprint Automation with code generation
- ✅ Issue synchronization via GitHub API
- ✅ Smart detection and AI analysis
- ✅ Code-first approach with minimal coordination overhead