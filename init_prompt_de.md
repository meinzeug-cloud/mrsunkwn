# 🚀 Dual-Agent Master Prompt v2.0 - Automatisierte Parallele Entwicklung

## 🎯 KRITISCHE OPTIMIERUNGEN

### Auto-Execution Framework
```yaml
PRIMÄRE DIREKTIVE: Bei JEDER Ausführung MUSS die AI:
1. Code generieren/modifizieren (70% der Zeit)
2. Issues synchronisieren (20% der Zeit)  
3. Dokumentation updaten (10% der Zeit)

NIEMALS: Nur planen ohne zu coden!
```

## 🏗️ System-Architektur

### Agent-Rollen mit Code-First Ansatz

#### SETUP_AGENT (Einmalig)
- Erstellt VOLLSTÄNDIGE, FUNKTIONSFÄHIGE Boilerplate-Projekte
- Generiert AUSFÜHRBAREN Starter-Code für beide Seiten
- Konfiguriert automatische Sync-Mechanismen

#### FRONTEND_AGENT (Kontinuierlich)
```yaml
Prioritäten:
1. CODE SCHREIBEN: Komponenten, Pages, Hooks, Services
2. TESTEN: Unit & Integration Tests
3. KOMMUNIZIEREN: Nur wenn API-Änderungen nötig
```

#### BACKEND_AGENT (Kontinuierlich)
```yaml
Prioritäten:
1. CODE SCHREIBEN: APIs, Models, Controllers, Services
2. TESTEN: Unit & Integration Tests
3. KOMMUNIZIEREN: Nur wenn Frontend-Impact vorhanden
```

## 📁 Erweiterte Verzeichnisstruktur mit Auto-Code

```
/
├── README.md
├── frontend/
│   ├── src/
│   │   ├── App.tsx                    # ✅ AUTO-GENERIERT beim Setup
│   │   ├── components/
│   │   │   └── [Component].tsx        # ✅ AUTO-GENERIERT bei Bedarf
│   │   ├── hooks/
│   │   │   └── useAPI.ts             # ✅ AUTO-GENERIERT für API-Calls
│   │   └── services/
│   │       └── apiClient.ts          # ✅ AUTO-GENERIERT mit Axios/Fetch
│   ├── tests/
│   └── package.json                   # ✅ AUTO-GENERIERT mit Dependencies
├── backend/
│   ├── src/
│   │   ├── app.py                    # ✅ AUTO-GENERIERT beim Setup
│   │   ├── models/
│   │   │   └── [Model].py           # ✅ AUTO-GENERIERT bei Bedarf
│   │   ├── controllers/
│   │   │   └── [Controller].py      # ✅ AUTO-GENERIERT bei Bedarf
│   │   └── routes/
│   │       └── api.py               # ✅ AUTO-GENERIERT mit Endpoints
│   ├── tests/
│   └── requirements.txt              # ✅ AUTO-GENERIERT mit Dependencies
└── codex/
    ├── automation/
    │   ├── code_generator.py         # ✅ AUTO-CODE Generator
    │   ├── issue_sync.py            # ✅ AUTO-SYNC zwischen Agents
    │   └── sprint_runner.py         # ✅ AUTO-SPRINT Executor
    └── templates/
        ├── frontend/                 # Code-Templates für Frontend
        └── backend/                  # Code-Templates für Backend
```

## 🤖 PHASE 1: Setup mit Auto-Code Generation

### Setup-Agent Prompt (OPTIMIERT):
```bash
codex "Führe Dual-Agent Setup durch und GENERIERE SOFORT funktionsfähigen Starter-Code für beide Seiten"
```

### Setup-Agent Auto-Aktionen:

```python
# 1. AUTOMATISCHE CODE-GENERIERUNG (NEU!)
def generate_starter_code():
    """Generiert SOFORT lauffähigen Code"""
    
    # Frontend Starter (React/TypeScript)
    create_file('/frontend/src/App.tsx', """
import React, { useEffect, useState } from 'react';
import { apiClient } from './services/apiClient';

function App() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    apiClient.get('/api/status').then(res => setData(res.data));
  }, []);
  
  return (
    <div className="App">
      <h1>Dual-Agent Project</h1>
      <p>Status: {data?.status || 'Loading...'}</p>
    </div>
  );
}
export default App;
    """)
    
    # Backend Starter (Python/FastAPI)
    create_file('/backend/src/app.py', """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
async def get_status():
    return {"status": "operational", "version": "1.0.0"}

@app.get("/api/data")
async def get_data():
    # TODO: Implement data endpoint
    return {"data": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    """)
    
    # API Client für Frontend
    create_file('/frontend/src/services/apiClient.ts', """
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
    """)

# 2. AUTO-SYNC SYSTEM (OPTIMIERT)
def create_auto_sync_system():
    """Erstellt automatisches Agent-Sync System"""
    
    create_file('/codex/automation/issue_sync.py', """
import os
import json
import subprocess
from datetime import datetime

class AgentSync:
    def __init__(self):
        self.frontend_watch = '/codex/daten/frontend/requests.json'
        self.backend_watch = '/codex/daten/backend/requests.json'
    
    def auto_create_issue(self, from_agent, to_agent, request_type, details):
        '''Erstellt automatisch GitHub Issue'''
        
        # Auto-detect API changes
        if request_type == 'api_change':
            title = f"🔄 API Change: {details['endpoint']}"
            labels = ['api-contract', f'{to_agent.lower()}-request']
        elif request_type == 'new_feature':
            title = f"✨ New Feature: {details['feature']}"
            labels = [f'{to_agent.lower()}-request', 'enhancement']
        else:
            title = f"📋 {from_agent} → {to_agent}: {details['title']}"
            labels = [f'{to_agent.lower()}-request']
        
        # Create issue via CURL
        issue_data = {
            'title': title,
            'body': self._generate_issue_body(from_agent, details),
            'labels': labels
        }
        
        curl_cmd = [
            'curl', '-s', '-X', 'POST',
            '-H', f'Authorization: token {os.getenv("GITHUB_TOKEN")}',
            '-H', 'Accept: application/vnd.github.v3+json',
            '-d', json.dumps(issue_data),
            f'https://api.github.com/repos/{os.getenv("REPO_OWNER")}/{os.getenv("REPO_NAME")}/issues'
        ]
        
        subprocess.run(curl_cmd)
    
    def _generate_issue_body(self, from_agent, details):
        '''Generiert strukturierten Issue Body'''
        return f'''
## 🤖 Auto-Generated by {from_agent}

### Request Type: {details.get('type', 'general')}

### Details:
{json.dumps(details, indent=2)}

### Expected Response:
- [ ] Acknowledge receipt
- [ ] Implement changes
- [ ] Update API contracts if needed
- [ ] Notify completion

### Auto-Sync ID: {datetime.now().isoformat()}
'''

# Auto-Sync Runner
if __name__ == '__main__':
    sync = AgentSync()
    # Wird bei jedem Sprint automatisch ausgeführt
    """)

# 3. SPRINT AUTOMATION (NEU!)
def create_sprint_automation():
    """Sprint Runner für automatische Ausführung"""
    
    create_file('/codex/automation/sprint_runner.py', """
import os
import sys
import time
from datetime import datetime

class SprintRunner:
    def __init__(self, agent_role):
        self.agent = agent_role
        self.sprint_count = 0
        
    def run_sprint(self):
        '''Führt einen kompletten Sprint automatisch aus'''
        self.sprint_count += 1
        print(f"\\n🏃 Sprint #{self.sprint_count} - {self.agent}")
        
        # 1. Issue Sync
        self._sync_issues()
        
        # 2. Analyze & Prioritize
        tasks = self._prioritize_tasks()
        
        # 3. GENERATE CODE (WICHTIGSTER TEIL!)
        for task in tasks:
            if task['type'] in ['feature', 'api', 'component']:
                self._generate_code(task)
            elif task['type'] == 'bug':
                self._fix_code(task)
                
        # 4. Run Tests
        self._run_tests()
        
        # 5. Update Status
        self._update_status()
        
    def _generate_code(self, task):
        '''GENERIERT TATSÄCHLICHEN CODE'''
        print(f"💻 Generating code for: {task['title']}")
        
        if self.agent == 'FRONTEND_AGENT':
            if 'component' in task['title'].lower():
                self._create_react_component(task)
            elif 'page' in task['title'].lower():
                self._create_react_page(task)
            elif 'hook' in task['title'].lower():
                self._create_react_hook(task)
                
        elif self.agent == 'BACKEND_AGENT':
            if 'endpoint' in task['title'].lower():
                self._create_api_endpoint(task)
            elif 'model' in task['title'].lower():
                self._create_data_model(task)
            elif 'service' in task['title'].lower():
                self._create_service(task)
    
    def _create_react_component(self, task):
        '''Generiert React Component'''
        component_name = task.get('component_name', 'NewComponent')
        code = f'''
import React from 'react';
import {{ useAPI }} from '../hooks/useAPI';

interface {component_name}Props {{
  // TODO: Define props
}}

export const {component_name}: React.FC<{component_name}Props> = (props) => {{
  const {{ data, loading, error }} = useAPI('/api/{component_name.lower()}');
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {{error.message}}</div>;
  
  return (
    <div className="{component_name.lower()}">
      {{/* TODO: Implement component */}}
      <h2>{component_name}</h2>
      <pre>{{JSON.stringify(data, null, 2)}}</pre>
    </div>
  );
}};
'''
        # Speichere Component
        path = f'/frontend/src/components/{component_name}.tsx'
        self._save_code(path, code)
        
# Sprint Executor
if __name__ == '__main__':
    agent = os.getenv('AGENT_ROLE')
    runner = SprintRunner(agent)
    runner.run_sprint()
    """)
```

## 🎯 PHASE 2: Agent-Prompts mit Auto-Execution

### FRONTEND Agent Prompt (OPTIMIERT):
```markdown
# Frontend Agent - CODE FIRST!

## 🚨 WICHTIGSTE REGEL
Bei JEDER Ausführung MUSST du:
1. **CODE GENERIEREN** (mindestens 1 neue Komponente/Feature)
2. **TESTS SCHREIBEN** (für generierten Code)
3. **NUR DANN** Issues erstellen, wenn Backend-Änderung nötig

## Auto-Sprint Execution

```python
# AUTOMATISCH bei jedem Start ausführen:
import sys
sys.path.append('/codex/automation/')
from sprint_runner import SprintRunner
from issue_sync import AgentSync

# Sprint starten
runner = SprintRunner('FRONTEND_AGENT')
runner.run_sprint()

# Nach Code-Generierung: Sync prüfen
sync = AgentSync()
# Automatisch Issues für API-Anfragen erstellen
```

## Tägliche Code-Ziele
- [ ] Mindestens 2 neue Components
- [ ] Mindestens 1 neuer Hook
- [ ] Mindestens 3 Unit Tests
- [ ] API Integration für neue Endpoints

## Code-Generation Triggers
- Neues Issue → Sofort Component erstellen
- API Contract Update → Sofort Service anpassen
- Bug Report → Sofort Fix implementieren

## NIEMALS
- ❌ Nur planen ohne Code zu schreiben
- ❌ Auf Backend warten ohne Frontend vorzubereiten
- ❌ Issues erstellen ohne konkreten Bedarf
```

### BACKEND Agent Prompt (OPTIMIERT):
```markdown
# Backend Agent - API FIRST!

## 🚨 WICHTIGSTE REGEL
Bei JEDER Ausführung MUSST du:
1. **APIs IMPLEMENTIEREN** (mindestens 1 neuer Endpoint)
2. **MODELS ERSTELLEN** (für neue Features)
3. **NUR DANN** Issues erstellen, wenn Frontend-Info nötig

## Auto-Sprint Execution

```python
# AUTOMATISCH bei jedem Start ausführen:
import sys
sys.path.append('/codex/automation/')
from sprint_runner import SprintRunner
from issue_sync import AgentSync

# Sprint starten
runner = SprintRunner('BACKEND_AGENT')
runner.run_sprint()

# Nach API-Erstellung: Contracts updaten
with open('/codex/daten/shared/api_contracts.md', 'a') as f:
    f.write(f"\\n## Neuer Endpoint: {endpoint_info}")
```

## Tägliche Code-Ziele
- [ ] Mindestens 2 neue API Endpoints
- [ ] Mindestens 1 neues Model
- [ ] Mindestens 1 Service Layer
- [ ] Database Migrations wenn nötig

## Code-Generation Triggers
- Frontend Request → Sofort API erstellen
- Neues Feature → Sofort Model + Controller
- Performance Issue → Sofort Optimierung

## NIEMALS
- ❌ Nur Datenbank-Design ohne Implementation
- ❌ Warten auf perfekte Spezifikation
- ❌ Issues ohne konkreten Code dahinter
```

## 🔄 Automatischer Sprint-Zyklus 2.0

### Start-Kommandos (VEREINFACHT):

```bash
# Setup (einmalig)
export GITHUB_TOKEN=xxx REPO_OWNER=xxx REPO_NAME=xxx
codex "Setup Dual-Agent System - generiere Starter Code"

# Frontend Agent (wiederholt)
export AGENT_ROLE=FRONTEND_AGENT
codex "Starte Frontend Sprint - schreibe Code"

# Backend Agent (wiederholt)  
export AGENT_ROLE=BACKEND_AGENT
codex "Starte Backend Sprint - schreibe APIs"
```

### Auto-Features:

1. **Code-First Approach**
   - Jeder Sprint MUSS Code generieren
   - Templates für schnelle Generierung
   - Auto-Import von Dependencies

2. **Smart Issue Creation**
   - Nur wenn Code-Abhängigkeit besteht
   - Auto-Detection von API-Änderungen
   - Strukturierte Request-Formate

3. **Continuous Integration**
   - Auto-Tests nach Code-Generierung
   - Auto-Merge bei erfolgreichen Tests
   - Auto-Deploy Vorbereitung

## 📊 Erfolgs-Metriken

```yaml
Pro Sprint MINIMUM:
- Lines of Code: 200+
- Neue Features: 2+
- Tests: 5+
- Issues: Max 2 (nur wenn nötig)

FOKUS: 80% Coding, 20% Koordination
```

## 🚀 Zusammenfassung der Optimierungen

1. **CODE FIRST**: Agents müssen bei jeder Ausführung Code generieren
2. **AUTO-SYNC**: Automatische Issue-Erstellung nur bei Bedarf
3. **SMART TEMPLATES**: Vorgefertigte Code-Templates für schnelle Entwicklung
4. **SPRINT AUTOMATION**: Komplette Sprint-Ausführung automatisiert
5. **CLEAR PRIORITIES**: Coding > Testing > Communication

Das System garantiert jetzt:
- ✅ Bei JEDER Ausführung wird Code geschrieben
- ✅ Automatische Synchronisation ohne manuelle Intervention  
- ✅ Klare Metriken für Fortschritt
- ✅ Minimale Koordinations-Overhead
- ✅ Maximale Code-Output