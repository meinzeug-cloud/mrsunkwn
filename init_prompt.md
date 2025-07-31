# Dual-Agent Master Prompt für parallele Frontend/Backend Entwicklung

## 🚀 System-Architektur

### Agent-Rollen (Phasenbasiert)

#### Phase 1: Initiale Setup (EINMALIG)
- **SETUP_AGENT**: Konfiguriert komplette Dual-Agent Infrastruktur
  - Erstellt Verzeichnisstruktur
  - GitHub Repository Setup
  - Agent-Konfigurationsdateien
  - Issue-Management System
  - **WICHTIG**: Übernimmt KEINE spezifische Agent-Rolle

#### Phase 2: Parallele Entwicklung (KONTINUIERLICH)
- **FRONTEND_AGENT**: UI/UX, Client-seitige Logik, API-Integration
- **BACKEND_AGENT**: Server-Logik, Datenbank, APIs, Services

### Kommunikationsprotokoll
- **GitHub Issues** als primäres Kommunikationsmittel zwischen Agents
- **Branch-basierte Entwicklung**: `feature/frontend-*` und `feature/backend-*`
- **Automatische Issue-Synchronisation** bei jedem Sprint

## 📁 Verzeichnisstruktur (wird vom SETUP_AGENT erstellt)

```
/
├── README.md                           # Projektkonzept (MUSS bereits existieren)
├── frontend/                          # Frontend-Code
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── package.json
├── backend/                           # Backend-Code
│   ├── src/
│   ├── models/
│   ├── controllers/
│   ├── routes/
│   └── requirements.txt
└── codex/
    ├── agents/
    │   ├── frontend/
    │   │   ├── config.md              # Frontend-Agent Konfiguration
    │   │   └── prompt.md              # Frontend-Agent Ausführungs-Prompt
    │   ├── backend/
    │   │   ├── config.md              # Backend-Agent Konfiguration
    │   │   └── prompt.md              # Backend-Agent Ausführungs-Prompt
    │   └── setup/
    │       ├── config.md              # Setup-Agent Konfiguration
    │       └── validation.md          # Setup-Validierung
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
        ├── github_config.py           # GitHub API Konfiguration
        └── issue_manager.py           # Issue Management Script
```

## 🎯 PHASE 1: Setup-Agent Ausführung (EINMALIG)

### WICHTIG: Setup-Voraussetzungen

**Manuelle Vorbereitung ERFORDERLICH:**
1. **GitHub Repository** bereits erstellt und zugänglich
2. **README.md** mit vollständiger Projektbeschreibung bereits vorhanden
3. **Umgebungsvariablen** müssen gesetzt sein:
   ```bash
   export GITHUB_TOKEN=your_personal_access_token
   export REPO_OWNER=your_github_username  
   export REPO_NAME=your_repository_name
   ```

### Setup-Agent Ausführung:
```bash
# KEINE Agent-Rolle setzen - Setup-Agent arbeitet neutral
codex "Führe Setup für Dual-Agent System durch basierend auf diesem Master-Prompt"
```

### Setup-Agent Aufgaben (Automatisch ausgeführt):

#### 1. Projekt-Analyse & Validierung
```python
# Setup-Agent führt aus:
def validate_prerequisites():
    # ✅ GitHub Repository Zugang testen
    # ✅ README.md existiert und ist vollständig
    # ✅ Umgebungsvariablen vorhanden
    # ✅ GitHub API Funktionalität testen
```

#### 2. GitHub Repository Konfiguration
```python
def setup_github_repository():
    # ✅ 9 Agent-Kommunikations-Labels erstellen:
    labels = [
        'frontend-request', 'backend-request', 'api-contract',
        'integration', 'bug-cross-agent', 'documentation',
        'setup-required', 'sprint-coordination', 'validation-needed'
    ]
    
    # ✅ Branch-Struktur erstellen
    branches = ['develop-frontend', 'develop-backend']
    
    # ✅ Branch Protection Rules
    # ✅ Issue Templates erstellen
```

#### 3. Verzeichnisstruktur Generierung
```python
def create_directory_structure():
    # ✅ Komplette /codex/ Struktur erstellen
    # ✅ Alle notwendigen .md Dateien generieren
    # ✅ Python Scripts für GitHub Integration
    # ✅ Agent-spezifische Konfigurationsdateien
```

#### 4. Agent-Konfigurationsdateien erstellen

**Frontend Agent Konfiguration** (`/codex/agents/frontend/config.md`):
```markdown
# Frontend Agent Konfiguration

## Verantwortlichkeiten
- UI/UX Entwicklung
- Client-seitige Logik
- API Integration
- Frontend Testing
- Responsive Design

## Technologie-Stack
[Wird basierend auf README.md befüllt]

## GitHub Issue Labels (Frontend)
- `frontend-request`: Anfragen an Backend
- `api-contract`: API-Definitionen
- `integration`: Frontend-Backend Integration
```

**Backend Agent Konfiguration** (`/codex/agents/backend/config.md`):
```markdown
# Backend Agent Konfiguration

## Verantwortlichkeiten
- Server-Logik
- Datenbank Design & Management
- API Entwicklung
- Backend Services
- Performance & Security

## Technologie-Stack
[Wird basierend auf README.md befüllt]

## GitHub Issue Labels (Backend)
- `backend-request`: Anfragen an Frontend
- `api-contract`: API-Definitionen
- `integration`: Backend-Frontend Integration
```

#### 5. Ausführbare Agent-Prompts generieren

**Frontend Agent Prompt** (`/codex/agents/frontend/prompt.md`):
```markdown
# Frontend Agent Ausführungs-Prompt

## Agent-Identifikation
Du bist der **FRONTEND_AGENT** in einem Dual-Agent System.

## Sprint-Start Protokoll

### 1. Agent-Rolle setzen
```bash
export AGENT_ROLE=FRONTEND_AGENT
```

### 2. Issue-Synchronisation (bei JEDEM Sprint)
```python
# Automatische Ausführung:
import sys
sys.path.append('/codex/github/')
from issue_manager import sync_frontend_issues

# GitHub Issues für Frontend laden
my_issues = sync_frontend_issues()
print(f"Gefundene Frontend Issues: {len(my_issues)}")
```

### 3. Roadmap Check
- Lese: `/codex/daten/frontend/roadmap.md`
- Lese: `/codex/daten/frontend/status.md`
- Lese: `/codex/daten/shared/api_contracts.md`

### 4. Arbeitsbereich
- Arbeite AUSSCHLIESSLICH in: `/frontend/`
- Branch: `feature/frontend-*`
- Tests: Frontend-spezifische Tests

### 5. Koordination
- Erstelle Issues für Backend-Anfragen
- Update API-Contracts bei Änderungen
- Kommuniziere über GitHub Issues

### 6. Sprint-Ende
- Update `/codex/daten/frontend/changelog.md`
- Update `/codex/daten/frontend/status.md`
- Erstelle Issues für nächsten Sprint
```

**Backend Agent Prompt** (`/codex/agents/backend/prompt.md`):
```markdown
# Backend Agent Ausführungs-Prompt

## Agent-Identifikation
Du bist der **BACKEND_AGENT** in einem Dual-Agent System.

## Sprint-Start Protokoll

### 1. Agent-Rolle setzen
```bash
export AGENT_ROLE=BACKEND_AGENT
```

### 2. Issue-Synchronisation (bei JEDEM Sprint)
```python
# Automatische Ausführung:
import sys
sys.path.append('/codex/github/')
from issue_manager import sync_backend_issues

# GitHub Issues für Backend laden
my_issues = sync_backend_issues()
print(f"Gefundene Backend Issues: {len(my_issues)}")
```

### 3. Roadmap Check
- Lese: `/codex/daten/backend/roadmap.md`
- Lese: `/codex/daten/backend/status.md`
- Lese: `/codex/daten/shared/api_contracts.md`

### 4. Arbeitsbereich
- Arbeite AUSSCHLIESSLICH in: `/backend/`
- Branch: `feature/backend-*`
- Tests: Backend-spezifische Tests

### 5. Koordination
- Erstelle Issues für Frontend-Benachrichtigungen
- Update API-Contracts bei neuen APIs
- Kommuniziere über GitHub Issues

### 6. Sprint-Ende
- Update `/codex/daten/backend/changelog.md`
- Update `/codex/daten/backend/status.md`
- Erstelle Issues für nächsten Sprint
```

#### 6. GitHub Issue Management System

**Issue Manager Script** (`/codex/github/issue_manager.py`):
```python
import os
import requests
from datetime import datetime

# Globale Umgebungsvariablen (bereits gesetzt)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')

def sync_frontend_issues():
    """Lädt alle Frontend-relevanten Issues"""
    issues = fetch_issues_by_labels(['frontend-request', 'api-contract', 'integration'])
    return filter_open_issues(issues)

def sync_backend_issues():
    """Lädt alle Backend-relevanten Issues"""
    issues = fetch_issues_by_labels(['backend-request', 'api-contract', 'integration'])
    return filter_open_issues(issues)

def create_coordination_issue(title, body, labels, assignee=None):
    """Erstellt neues Issue für Agent-Koordination"""
    # GitHub API Implementation
    pass

def close_completed_issue(issue_number, completion_note):
    """Schließt erledigte Issues"""
    # GitHub API Implementation
    pass
```

#### 7. Setup-Validierung & Abschluss

```python
def validate_setup():
    # ✅ Alle Verzeichnisse erstellt
    # ✅ Alle Konfigurationsdateien vorhanden
    # ✅ GitHub API funktional
    # ✅ Issue-Labels erstellt
    # ✅ Branch-Struktur vorhanden
    # ✅ Agent-Prompts ausführbar
```

#### 8. Erstes Koordinations-Issue erstellen

```markdown
**Titel**: "🚀 Dual-Agent System Setup abgeschlossen - Bereit für parallele Entwicklung"
**Labels**: setup-required, sprint-coordination
**Body**:
# Dual-Agent System erfolgreich konfiguriert!

## ✅ Setup-Agent Abschluss

### Konfigurierte Komponenten:
- ✅ GitHub Repository mit 9 Agent-Labels
- ✅ Branch-Struktur (develop-frontend, develop-backend)
- ✅ Komplette /codex/ Verzeichnisstruktur
- ✅ Agent-Konfigurationsdateien
- ✅ Ausführbare Agent-Prompts
- ✅ GitHub Issue Management System
- ✅ API-Contract Management

### Nächste Schritte:

#### Frontend Agent Start:
```bash
codex führe prompt /codex/agents/frontend/prompt.md
```

#### Backend Agent Start:
```bash
codex führe prompt /codex/agents/backend/prompt.md
```

**System ist bereit für parallele Dual-Agent Entwicklung!**
```

## 🎯 PHASE 2: Parallele Agent-Entwicklung

### Frontend Agent starten:
```bash
# Terminal 1
codex führe prompt /codex/agents/frontend/prompt.md
```

### Backend Agent starten:
```bash
# Terminal 2  
codex führe prompt /codex/agents/backend/prompt.md
```

## 🔄 Kontinuierlicher Sprint-Zyklus (für beide Agents)

### Bei jedem Sprint automatisch:
1. **Issue-Synchronisation**: Laden aller relevanten GitHub Issues
2. **Roadmap-Check**: Aktuelle Aufgaben aus Roadmap
3. **API-Contract Check**: Aktuelle API-Definitionen
4. **Koordinations-Issues**: Neue Issues für anderen Agent erstellen
5. **Entwicklung**: Arbeit an zugewiesenen Aufgaben
6. **Dokumentation**: Changelog und Status Updates
7. **Issue-Updates**: Erledigte Issues schließen, neue erstellen

### Agent-Kommunikation über GitHub Issues:
- **Frontend → Backend**: Issues mit Label `backend-request`
- **Backend → Frontend**: Issues mit Label `frontend-request`
- **Gemeinsam**: Issues mit Label `integration`, `api-contract`

## 🚀 Zusammenfassung der Ausführung

### 1. Einmalige Setup-Phase:
```bash
# Umgebungsvariablen setzen (einmalig)
export GITHUB_TOKEN=your_token
export REPO_OWNER=your_username
export REPO_NAME=your_repo

# Setup-Agent ausführen (einmalig)
codex "Führe Setup für Dual-Agent System durch basierend auf diesem Master-Prompt"
```

### 2. Parallele Entwicklungsphase (wiederholbar):
```bash
# Terminal 1 - Frontend Agent
codex führe prompt /codex/agents/frontend/prompt.md

# Terminal 2 - Backend Agent  
codex führe prompt /codex/agents/backend/prompt.md
```

**Das System gewährleistet:**
- ✅ Klare Trennung zwischen Setup und Entwicklung
- ✅ Automatische Agent-Koordination über GitHub Issues
- ✅ Parallele Entwicklung ohne Konflikte
- ✅ Kontinuierliche Integration und Kommunikation
- ✅ Vollständige Dokumentation und Nachverfolgung

Die Agents arbeiten völlig autonom in ihren Bereichen und koordinieren sich automatisch über das GitHub Issue System!