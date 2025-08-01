import os
import json
import subprocess
from datetime import datetime

class AgentSync:
    def __init__(self):
        self.frontend_watch = '/codex/data/frontend/requests.json'
        self.backend_watch = '/codex/data/backend/requests.json'
    
    def auto_create_issue(self, from_agent, to_agent, request_type, details):
        '''Automatically creates GitHub issue'''
        
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
        '''Generates structured issue body'''
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
    # Runs automatically on every sprint