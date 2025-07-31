"""
Enhanced GitHub Issues Management for Mrs-Unkwn Development
"""
import os
import json
import subprocess
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

class MrsUnkwnIssueManager:
    """
    Enhanced issue management system aligned with Mrs-Unkwn roadmap
    """
    
    def __init__(self):
        self.repo_owner = os.getenv("REPO_OWNER", "meinzeug-cloud")
        self.repo_name = os.getenv("REPO_NAME", "mrsunkwn")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.project_root = Path('/home/runner/work/mrsunkwn/mrsunkwn')
        
        # Mrs-Unkwn specific issue templates
        self.issue_templates = {
            "ai_feature": {
                "labels": ["ai-feature", "enhancement", "mrs-unkwn-core"],
                "template": self._ai_feature_template
            },
            "anti_cheat": {
                "labels": ["anti-cheat", "security", "monitoring", "mrs-unkwn-core"],
                "template": self._anti_cheat_template
            },
            "parental_controls": {
                "labels": ["parental-controls", "security", "family", "mrs-unkwn-core"],
                "template": self._parental_controls_template
            },
            "device_monitoring": {
                "labels": ["device-monitoring", "tracking", "security", "mrs-unkwn-core"],
                "template": self._device_monitoring_template
            },
            "learning_analytics": {
                "labels": ["analytics", "learning", "data", "mrs-unkwn-core"],
                "template": self._learning_analytics_template
            },
            "api_endpoint": {
                "labels": ["api", "backend", "endpoint"],
                "template": self._api_endpoint_template
            },
            "ui_component": {
                "labels": ["ui", "frontend", "component"],
                "template": self._ui_component_template
            },
            "database": {
                "labels": ["database", "backend", "data"],
                "template": self._database_template
            },
            "testing": {
                "labels": ["testing", "quality", "automation"],
                "template": self._testing_template
            },
            "roadmap_milestone": {
                "labels": ["roadmap", "milestone", "planning"],
                "template": self._roadmap_milestone_template
            }
        }
    
    def create_roadmap_issues(self, roadmap_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create issues based on roadmap phases"""
        created_issues = []
        
        if not self._validate_github_access():
            logger.warning("GitHub access not available, creating local tracking")
            return self._create_local_issues(roadmap_data)
        
        try:
            for phase in roadmap_data.get('phases', []):
                # Create milestone for phase
                milestone = self._create_milestone(phase)
                
                # Create issues for high-priority tasks
                for task in phase.get('tasks', [])[:10]:  # Limit to first 10 tasks per phase
                    issue = self._create_task_issue(task, phase, milestone)
                    if issue:
                        created_issues.append(issue)
            
            # Create meta-issues for tracking
            meta_issues = self._create_meta_issues(roadmap_data)
            created_issues.extend(meta_issues)
            
            return created_issues
            
        except Exception as e:
            logger.error(f"Error creating roadmap issues: {str(e)}")
            return self._create_local_issues(roadmap_data)
    
    def _create_task_issue(self, task: Dict[str, Any], phase: Dict[str, Any], milestone: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create GitHub issue for a specific task"""
        try:
            task_type = task.get('type', 'feature')
            template_key = self._map_task_type_to_template(task_type)
            
            if template_key not in self.issue_templates:
                template_key = 'api_endpoint'  # default
            
            template_config = self.issue_templates[template_key]
            
            # Generate title
            title = f"🏗️ {phase['title']}: {task['description'][:80]}"
            
            # Generate body using template
            body = template_config['template'](task, phase)
            
            # Prepare labels
            labels = template_config['labels'].copy()
            labels.append(f"phase-{phase['id']}")
            
            # Create the issue
            issue_data = {
                "title": title,
                "body": body,
                "labels": labels,
                "milestone": milestone['number'] if milestone else None
            }
            
            # Make API call
            response = self._make_github_api_call("POST", "issues", issue_data)
            
            if response:
                logger.info(f"Created issue: {title}")
                return response
            
        except Exception as e:
            logger.error(f"Error creating task issue: {str(e)}")
        
        return None
    
    def _create_milestone(self, phase: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create milestone for roadmap phase"""
        try:
            milestone_data = {
                "title": f"Phase {phase['id']}: {phase['title']}",
                "description": f"Implementation of Mrs-Unkwn Phase {phase['id']} features and components",
                "due_on": (datetime.now() + timedelta(days=30 * phase['id'])).isoformat()
            }
            
            response = self._make_github_api_call("POST", "milestones", milestone_data)
            
            if response:
                logger.info(f"Created milestone: {milestone_data['title']}")
                return response
                
        except Exception as e:
            logger.error(f"Error creating milestone: {str(e)}")
        
        return None
    
    def _create_meta_issues(self, roadmap_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create meta-issues for overall tracking"""
        meta_issues = []
        
        # Development progress tracking issue
        progress_issue = {
            "title": "📊 Mrs-Unkwn Development Progress Tracker",
            "body": self._progress_tracker_template(roadmap_data),
            "labels": ["tracking", "progress", "meta", "pinned"]
        }
        
        response = self._make_github_api_call("POST", "issues", progress_issue)
        if response:
            meta_issues.append(response)
        
        # Architecture decisions issue
        architecture_issue = {
            "title": "🏛️ Mrs-Unkwn Architecture Decisions & Technical Debt",
            "body": self._architecture_template(),
            "labels": ["architecture", "technical-debt", "meta"]
        }
        
        response = self._make_github_api_call("POST", "issues", architecture_issue)
        if response:
            meta_issues.append(response)
        
        return meta_issues
    
    def _make_github_api_call(self, method: str, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make GitHub API call"""
        if not self.github_token:
            return None
        
        try:
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/{endpoint}"
            
            curl_cmd = [
                'curl', '-s', '-X', method,
                '-H', f'Authorization: token {self.github_token}',
                '-H', 'Accept: application/vnd.github.v3+json',
                '-d', json.dumps(data),
                url
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                logger.error(f"GitHub API call failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error making GitHub API call: {str(e)}")
            return None
    
    def _validate_github_access(self) -> bool:
        """Validate GitHub API access"""
        if not self.github_token:
            return False
        
        try:
            response = self._make_github_api_call("GET", "", {})
            return response is not None
        except:
            return False
    
    def _create_local_issues(self, roadmap_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create local issue tracking when GitHub is not available"""
        local_issues = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create comprehensive local tracking
        issues_dir = self.project_root / "codex" / "data" / "issues"
        issues_dir.mkdir(parents=True, exist_ok=True)
        
        for phase in roadmap_data.get('phases', []):
            phase_file = issues_dir / f"phase_{phase['id']}_{timestamp}.md"
            
            phase_content = f"""# Phase {phase['id']}: {phase['title']}

**Status**: 📋 Planning
**Priority**: High
**Estimated Duration**: 4-6 weeks

## 🎯 Phase Objectives

{phase.get('description', 'Core Mrs-Unkwn development phase')}

## 📋 Tasks ({len(phase.get('tasks', []))})

"""
            
            for i, task in enumerate(phase.get('tasks', []), 1):
                task_type = task.get('type', 'feature')
                priority = self._determine_task_priority(task, task_type)
                
                phase_content += f"""### {i}. {task['description']}

- **Type**: {task_type}
- **Priority**: {priority}
- **Status**: ⏳ Pending
- **Estimated Effort**: {self._estimate_effort(task_type)}

**Acceptance Criteria**:
- [ ] Core functionality implemented
- [ ] Unit tests added
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Integration tested

---

"""
            
            with open(phase_file, 'w', encoding='utf-8') as f:
                f.write(phase_content)
            
            local_issues.append({
                "title": f"Phase {phase['id']}: {phase['title']}",
                "file": str(phase_file),
                "tasks": len(phase.get('tasks', []))
            })
        
        # Create master tracking file
        master_file = issues_dir / f"master_tracking_{timestamp}.md"
        master_content = f"""# Mrs-Unkwn Development Master Tracker

**Generated**: {datetime.now().isoformat()}
**Roadmap Phases**: {len(roadmap_data.get('phases', []))}
**Total Tasks**: {sum(len(phase.get('tasks', [])) for phase in roadmap_data.get('phases', []))}

## 🚀 Project Overview

Mrs-Unkwn is an AI-powered tutor app for teenagers (14+) focusing on:
- Socratic Method AI Tutoring
- Anti-Cheating Detection
- Parental Controls & Device Monitoring
- Learning Analytics & Progress Tracking
- Gamification & Engagement

## 📊 Development Status

"""
        
        for phase in roadmap_data.get('phases', []):
            progress = 0  # Calculate actual progress later
            master_content += f"- **Phase {phase['id']}**: {phase['title']} ({len(phase.get('tasks', []))} tasks) - {progress}% complete\n"
        
        master_content += f"""

## 🎯 Current Sprint Focus

Based on the roadmap, current development priorities are:

1. **AI Tutor Core** - Socratic Method implementation
2. **Anti-Cheat Engine** - Pattern detection and monitoring
3. **Parental Controls** - Family management and oversight
4. **Device Monitoring** - Activity tracking and alerts
5. **Learning Analytics** - Progress tracking and insights

## 📁 Phase Files

"""
        
        for issue in local_issues:
            master_content += f"- [{issue['title']}]({issue['file']}) - {issue['tasks']} tasks\n"
        
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write(master_content)
        
        logger.info(f"Created local issue tracking: {len(local_issues)} phase files")
        return local_issues
    
    # Template methods
    def _ai_feature_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 🤖 AI Feature Implementation

**Phase**: {phase['title']}
**Feature**: {task['description']}

### 🎯 Objective

Implement AI-powered functionality aligned with Mrs-Unkwn's Socratic Method approach.

### 📋 Requirements

- [ ] AI model integration (GPT-4 or equivalent)
- [ ] Socratic questioning logic
- [ ] Age-appropriate response filtering
- [ ] Learning progress tracking
- [ ] Performance metrics collection

### 🔧 Technical Specifications

- Use OpenAI API with custom prompts
- Implement response validation
- Add fallback mechanisms
- Include rate limiting
- Log all interactions for analytics

### ✅ Acceptance Criteria

- [ ] AI responses follow Socratic method
- [ ] No direct answers provided
- [ ] Age-appropriate content filtering
- [ ] Response time < 2 seconds
- [ ] Comprehensive error handling
- [ ] Integration tests passing

### 🧪 Testing Requirements

- [ ] Unit tests for AI logic
- [ ] Integration tests with API
- [ ] Load testing for performance
- [ ] Content appropriateness validation

---

*This is part of the Mrs-Unkwn roadmap implementation.*
"""

    def _anti_cheat_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 🛡️ Anti-Cheat System Implementation

**Phase**: {phase['title']}
**Component**: {task['description']}

### 🎯 Objective

Implement intelligent anti-cheating detection to maintain academic integrity.

### 📋 Requirements

- [ ] Pattern recognition algorithms
- [ ] Browser activity monitoring  
- [ ] Clipboard content analysis
- [ ] AI usage detection
- [ ] Behavioral anomaly detection
- [ ] Parent notification system

### 🔧 Technical Specifications

- Machine learning models for pattern detection
- Real-time monitoring capabilities
- Privacy-compliant data collection
- Configurable sensitivity levels
- Integration with parental controls

### ✅ Acceptance Criteria

- [ ] Accurate cheating detection (>85% precision)
- [ ] Low false positive rate (<10%)
- [ ] Real-time monitoring
- [ ] Privacy compliance (GDPR/COPPA)
- [ ] Parent dashboard integration
- [ ] Comprehensive logging

### 🧪 Testing Requirements

- [ ] Algorithm accuracy testing
- [ ] Performance benchmarking
- [ ] Privacy compliance validation
- [ ] Integration testing with monitoring

---

*Part of Mrs-Unkwn's academic integrity framework.*
"""

    def _parental_controls_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 👨‍👩‍👧‍👦 Parental Controls Implementation

**Phase**: {phase['title']}
**Feature**: {task['description']}

### 🎯 Objective

Provide comprehensive parental oversight and control features.

### 📋 Requirements

- [ ] Family account management
- [ ] Time limits and schedules
- [ ] Content filtering controls
- [ ] Activity monitoring dashboard
- [ ] Real-time alerts system
- [ ] Remote device control

### 🔧 Technical Specifications

- Role-based access control
- Real-time data synchronization
- Push notification system
- Granular permission settings
- Activity logging and reporting

### ✅ Acceptance Criteria

- [ ] Secure family account creation
- [ ] Granular control settings
- [ ] Real-time monitoring dashboard
- [ ] Instant alert notifications
- [ ] Remote control capabilities
- [ ] Data privacy compliance

### 🧪 Testing Requirements

- [ ] Access control testing
- [ ] Real-time sync validation
- [ ] Notification delivery testing
- [ ] Privacy compliance verification

---

*Empowering parents in their children's digital learning journey.*
"""

    def _device_monitoring_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 📱 Device Monitoring Implementation

**Phase**: {phase['title']}
**Component**: {task['description']}

### 🎯 Objective

Implement comprehensive device monitoring for educational context.

### 📋 Requirements

- [ ] App usage tracking
- [ ] Browser activity monitoring
- [ ] Screen time management
- [ ] Location-based controls
- [ ] Network activity analysis
- [ ] Privacy-compliant data collection

### 🔧 Technical Specifications

- Cross-platform monitoring (iOS/Android)
- Background service architecture
- Encrypted data transmission
- Local and cloud data storage
- Battery-efficient implementation

### ✅ Acceptance Criteria

- [ ] Accurate activity tracking
- [ ] Minimal battery impact (<5%)
- [ ] Privacy compliance
- [ ] Real-time data sync
- [ ] Comprehensive reporting
- [ ] Platform compatibility

### 🧪 Testing Requirements

- [ ] Battery usage testing
- [ ] Data accuracy validation
- [ ] Privacy compliance testing
- [ ] Cross-platform compatibility

---

*Balancing oversight with privacy in educational technology.*
"""

    def _learning_analytics_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 📊 Learning Analytics Implementation

**Phase**: {phase['title']}
**Component**: {task['description']}

### 🎯 Objective

Implement comprehensive learning analytics and progress tracking.

### 📋 Requirements

- [ ] Learning progress metrics
- [ ] Engagement pattern analysis
- [ ] Performance trend tracking
- [ ] Predictive analytics
- [ ] Personalized recommendations
- [ ] Visual reporting dashboard

### 🔧 Technical Specifications

- Data pipeline architecture
- Machine learning models
- Real-time analytics processing
- Interactive visualization
- Export capabilities

### ✅ Acceptance Criteria

- [ ] Accurate progress tracking
- [ ] Real-time analytics
- [ ] Predictive insights
- [ ] Interactive visualizations
- [ ] Export functionality
- [ ] Performance optimization

### 🧪 Testing Requirements

- [ ] Data accuracy validation
- [ ] Performance testing
- [ ] Visualization testing
- [ ] ML model validation

---

*Data-driven insights for personalized learning.*
"""

    def _api_endpoint_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 🔌 API Endpoint Implementation

**Phase**: {phase['title']}
**Endpoint**: {task['description']}

### 📋 Requirements

- [ ] RESTful API design
- [ ] Authentication & authorization
- [ ] Input validation
- [ ] Error handling
- [ ] Rate limiting
- [ ] API documentation

### ✅ Acceptance Criteria

- [ ] Full CRUD operations
- [ ] Proper HTTP status codes
- [ ] Comprehensive error handling
- [ ] API documentation
- [ ] Unit & integration tests

---

*Building robust APIs for Mrs-Unkwn platform.*
"""

    def _ui_component_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 🎨 UI Component Implementation

**Phase**: {phase['title']}
**Component**: {task['description']}

### 📋 Requirements

- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Mobile optimization
- [ ] User experience testing
- [ ] Cross-browser compatibility

### ✅ Acceptance Criteria

- [ ] WCAG 2.1 compliance
- [ ] Mobile responsiveness
- [ ] Cross-browser testing
- [ ] User testing validation

---

*Creating intuitive interfaces for teenagers and parents.*
"""

    def _database_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 🗄️ Database Implementation

**Phase**: {phase['title']}
**Component**: {task['description']}

### 📋 Requirements

- [ ] Database schema design
- [ ] Data migration scripts
- [ ] Performance optimization
- [ ] Backup strategies
- [ ] Security implementation

### ✅ Acceptance Criteria

- [ ] Normalized schema
- [ ] Migration scripts
- [ ] Performance benchmarks
- [ ] Security validation

---

*Robust data management for Mrs-Unkwn platform.*
"""

    def _testing_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 🧪 Testing Implementation

**Phase**: {phase['title']}
**Testing**: {task['description']}

### 📋 Requirements

- [ ] Unit test coverage
- [ ] Integration testing
- [ ] End-to-end testing
- [ ] Performance testing
- [ ] Security testing

### ✅ Acceptance Criteria

- [ ] 90%+ test coverage
- [ ] All tests passing
- [ ] Performance benchmarks met
- [ ] Security validation

---

*Quality assurance for Mrs-Unkwn platform.*
"""

    def _roadmap_milestone_template(self, task: Dict[str, Any], phase: Dict[str, Any]) -> str:
        return f"""## 🎯 Roadmap Milestone

**Phase**: {phase['title']}
**Milestone**: {task['description']}

### 📋 Requirements

- [ ] Milestone definition
- [ ] Success criteria
- [ ] Timeline planning
- [ ] Resource allocation
- [ ] Progress tracking

### ✅ Acceptance Criteria

- [ ] Clear deliverables
- [ ] Measurable outcomes
- [ ] Timeline adherence
- [ ] Quality standards met

---

*Strategic milestone in Mrs-Unkwn development roadmap.*
"""

    def _progress_tracker_template(self, roadmap_data: Dict[str, Any]) -> str:
        total_phases = len(roadmap_data.get('phases', []))
        total_tasks = sum(len(phase.get('tasks', [])) for phase in roadmap_data.get('phases', []))
        
        return f"""# 📊 Mrs-Unkwn Development Progress Tracker

**Last Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🎯 Overall Progress

- **Total Phases**: {total_phases}
- **Total Tasks**: {total_tasks}
- **Completed**: 0 (0%)
- **In Progress**: 0 (0%)
- **Pending**: {total_tasks} (100%)

## 📋 Phase Breakdown

"""
        content = roadmap_data.get('content', {})
        for phase in roadmap_data.get('phases', []):
            task_count = len(phase.get('tasks', []))
            content += f"""### Phase {phase['id']}: {phase['title']}
- **Tasks**: {task_count}
- **Status**: 📋 Planning
- **Progress**: 0%

"""
        
        content += """

## 🚀 Key Features Implementation Status

### Core Mrs-Unkwn Features
- [ ] AI Tutor with Socratic Method
- [ ] Anti-Cheating Detection Engine  
- [ ] Parental Controls Dashboard
- [ ] Device Monitoring System
- [ ] Learning Analytics Platform
- [ ] Gamification System
- [ ] Family Management
- [ ] Educational Content Management

### Technical Infrastructure
- [ ] Backend API (FastAPI)
- [ ] Frontend Application (React/Flutter)
- [ ] Database System (PostgreSQL)
- [ ] Authentication & Authorization
- [ ] Real-time Communication
- [ ] File Management
- [ ] Notification System
- [ ] Analytics Pipeline

## 📈 Sprint Progress

Track sprint-by-sprint progress here.

## 🎯 Next Milestones

1. **Phase 1 Completion**: Core AI tutor functionality
2. **Phase 2 Completion**: Anti-cheat engine
3. **Phase 3 Completion**: Parental controls
4. **Beta Release**: Limited testing with families
5. **Production Release**: Full public launch

---

*This tracker is automatically updated with each development sprint.*
"""

    def _architecture_template(self) -> str:
        return """# 🏛️ Mrs-Unkwn Architecture Decisions & Technical Debt

## 🏗️ Architecture Decisions

### Backend Architecture
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for session management
- **AI Integration**: OpenAI API with custom prompts
- **Authentication**: JWT with passlib/bcrypt

### Frontend Architecture  
- **Mobile**: Flutter for cross-platform development
- **Web**: React with TypeScript
- **State Management**: Provider (Flutter) / Redux (React)
- **UI Framework**: Material Design 3

### Infrastructure
- **Deployment**: Docker containers
- **Cloud**: Multi-cloud strategy (AWS/Azure/GCP)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with correlation IDs

## 📋 Technical Debt Tracking

### Current Debt Items
- [ ] Database migration strategy needs improvement
- [ ] API versioning strategy undefined
- [ ] Monitoring and alerting incomplete
- [ ] Security audit pending
- [ ] Performance optimization needed

### Code Quality Improvements
- [ ] Test coverage needs to reach 90%
- [ ] Documentation needs completion
- [ ] Code style guide enforcement
- [ ] Dependency management optimization
- [ ] Error handling standardization

## 🔒 Security Considerations

### Privacy & Compliance
- [ ] GDPR compliance implementation
- [ ] COPPA compliance for minors
- [ ] Data retention policies
- [ ] Encryption at rest and in transit
- [ ] Audit logging implementation

### Application Security
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Rate limiting implementation

---

*Maintaining high-quality architecture for Mrs-Unkwn platform.*
"""

    def _map_task_type_to_template(self, task_type: str) -> str:
        """Map task type to appropriate template"""
        mapping = {
            'ai_feature': 'ai_feature',
            'ai': 'ai_feature',
            'anti_cheat': 'anti_cheat',
            'security': 'anti_cheat',
            'parental_controls': 'parental_controls',
            'family': 'parental_controls',
            'device_monitoring': 'device_monitoring',
            'monitoring': 'device_monitoring',
            'analytics': 'learning_analytics',
            'learning': 'learning_analytics',
            'api': 'api_endpoint',
            'endpoint': 'api_endpoint',
            'component': 'ui_component',
            'ui': 'ui_component',
            'frontend': 'ui_component',
            'model': 'database',
            'database': 'database',
            'service': 'api_endpoint',
            'testing': 'testing',
            'milestone': 'roadmap_milestone'
        }
        
        return mapping.get(task_type, 'api_endpoint')
    
    def _determine_task_priority(self, task: Dict[str, Any], task_type: str) -> str:
        """Determine task priority based on type and content"""
        high_priority_types = ['ai_feature', 'anti_cheat', 'security', 'parental_controls']
        
        if task_type in high_priority_types:
            return "🔴 High"
        elif task_type in ['api', 'service', 'database']:
            return "🟡 Medium"
        else:
            return "🟢 Low"
    
    def _estimate_effort(self, task_type: str) -> str:
        """Estimate effort for task based on type"""
        effort_mapping = {
            'ai_feature': '2-3 days',
            'anti_cheat': '3-5 days',
            'parental_controls': '2-4 days',
            'device_monitoring': '3-4 days',
            'analytics': '2-3 days',
            'api': '1-2 days',
            'component': '1-2 days',
            'model': '0.5-1 day',
            'service': '1-2 days',
            'testing': '1 day'
        }
        
        return effort_mapping.get(task_type, '1-2 days')