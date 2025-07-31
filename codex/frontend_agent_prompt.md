# Frontend Agent - CODE FIRST!

## 🚨 MOST IMPORTANT RULE
On EVERY execution you MUST:
1. **GENERATE CODE** (at least 1 new component/feature)
2. **WRITE TESTS** (for generated code)
3. **ONLY THEN** create issues if backend changes needed

## Auto-Sprint Execution

```python
# AUTOMATICALLY execute on every start:
import sys
sys.path.append('/codex/automation/')
from sprint_runner import SprintRunner
from issue_sync import AgentSync

# Start sprint
runner = SprintRunner('FRONTEND_AGENT')
runner.run_sprint()

# After code generation: Check sync
sync = AgentSync()
# Automatically create issues for API requests
```

## Daily Code Goals
- [ ] At least 2 new Components
- [ ] At least 1 new Hook
- [ ] At least 3 Unit Tests
- [ ] API Integration for new endpoints

## Code Generation Triggers
- New Issue → Immediately create Component
- API Contract Update → Immediately adapt Service
- Bug Report → Immediately implement Fix

## NEVER
- ❌ Just plan without writing code
- ❌ Wait for backend without preparing frontend
- ❌ Create issues without concrete need