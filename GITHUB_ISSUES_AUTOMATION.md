# GitHub Issues Automation - Mrs-Unkwn

This document explains the GitHub Issues automation system implemented in the Mrs-Unkwn project.

## Overview

The autonomous development agent requires functional GitHub Issues integration to coordinate development tasks, plan next steps, and process feature requests. Without this integration, the agent cannot operate autonomously.

## How It Works

### 1. GitHub API Validation (`scripts/start_agent.sh`)

Before starting any development work, the script validates GitHub API connectivity:

```bash
# Test GitHub API connection
github_test_response=$(curl -s -w "%{http_code}" -o /tmp/github_test.json \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME" 2>/dev/null)
```

### 2. Behavior Based on Connectivity

#### ✅ GitHub API Available (HTTP 200)
- Validates repository access
- Sets `GITHUB_API_VALIDATED=true`
- Proceeds with normal autonomous operation
- Creates actual GitHub issues for planned tasks

#### ❌ GitHub API Unavailable (Any other status)
- **Normal Mode**: Stops execution with detailed error message
- **Test Mode**: Creates local issue tracking files instead

### 3. Issue Creation Process

When GitHub API is available, the system:

1. **Validates Credentials**: Checks token, repo owner, and repo name
2. **Generates Issues**: Creates GitHub issues for each planned task
3. **Tracks Success/Failure**: Monitors creation success rate
4. **Stops on Failure**: Halts if issue creation fails completely

### 4. Local Issue Tracking (Test Mode)

When GitHub API is unavailable but `TEST_MODE=true`:

- Creates local Markdown files in `codex/data/issues/`
- Generates comprehensive task lists with status tracking
- Creates JSON summaries for programmatic access
- Allows local development without GitHub dependency

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | Personal access token for GitHub API |
| `REPO_OWNER` | Yes | GitHub repository owner (username/org) |
| `REPO_NAME` | Yes | GitHub repository name |
| `TEST_MODE` | No | Set to `true` for local-only development |

## Usage

### Normal Operation (Requires GitHub API)
```bash
export GITHUB_TOKEN="your_personal_access_token"
export REPO_OWNER="your-username"
export REPO_NAME="your-repo-name"
./scripts/start_agent.sh
```

### Test Mode (Local Development Only)
```bash
export TEST_MODE=true
./scripts/start_agent.sh
```

## Error Handling

### GitHub API Connectivity Issues

Common causes and solutions:

1. **Invalid Token**: 
   - Error: HTTP 401/403
   - Solution: Generate new personal access token with repo permissions

2. **Network/Proxy Issues**:
   - Error: HTTP 403 "Blocked by DNS monitoring proxy"
   - Solution: Configure network access or use test mode

3. **Repository Access**:
   - Error: HTTP 404
   - Solution: Verify repo owner/name and token permissions

4. **Rate Limiting**:
   - Error: HTTP 429
   - Solution: Wait for rate limit reset or implement backoff

### Autonomous Operation Requirements

The system **requires** GitHub Issues for:

- **Planning Next Steps**: Issues track what needs to be implemented
- **Feature Requests**: Programmers can create issues for desired features
- **Development Coordination**: Issues coordinate work between different components
- **Progress Tracking**: Issues show what's completed vs. pending

Without functional GitHub Issues, the agent cannot operate autonomously and will stop execution.

## File Structure

### Generated Files

#### GitHub API Available
- GitHub issues created in the repository
- Issue URLs logged to console
- Sprint status saved to `codex/data/backend/sprint_status.md`

#### Test Mode
- `codex/data/issues/sprint_N_TIMESTAMP_issues.md` - Detailed task list
- `codex/data/issues/latest_sprint_summary.json` - Machine-readable summary

### Log Files
- Console output shows validation and creation status
- Error messages include detailed troubleshooting information

## Integration Points

### Sprint Runner (`codex/automation/sprint_runner.py`)

- `_sync_issues()`: Main issue synchronization method
- `_create_github_issue()`: Individual issue creation
- `_create_local_issue_tracking()`: Fallback for test mode

### Shell Script (`scripts/start_agent.sh`)

- GitHub API validation
- Environment variable management
- Error handling and user guidance

## Security Considerations

1. **Token Storage**: Store GitHub tokens securely, not in code
2. **Permissions**: Use tokens with minimal required permissions
3. **Local Files**: Local issue tracking files may contain sensitive task details
4. **Network**: Ensure secure network connections for API calls

## Troubleshooting

### Common Issues

1. **"Missing or dummy credentials"**
   - Check GITHUB_TOKEN, REPO_OWNER, REPO_NAME are set
   - Verify token is not placeholder value

2. **"GitHub API connectivity failed"**
   - Test manual curl command with your token
   - Check network connectivity to api.github.com

3. **"No GitHub issues could be created"**
   - Verify token has repository write permissions
   - Check repository exists and is accessible

### Debug Steps

1. **Test API Manually**:
   ```bash
   curl -H "Authorization: token YOUR_TOKEN" \
        https://api.github.com/repos/OWNER/REPO
   ```

2. **Check Token Permissions**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Verify token has "repo" scope

3. **Test Issue Creation**:
   ```bash
   curl -X POST -H "Authorization: token YOUR_TOKEN" \
        -d '{"title":"Test Issue","body":"Test"}' \
        https://api.github.com/repos/OWNER/REPO/issues
   ```

## Development Notes

The system is designed to fail fast and provide clear error messages when GitHub Issues automation is not functional. This ensures:

- No uncoordinated development occurs
- Clear guidance for fixing connectivity issues
- Fallback option (test mode) for local development
- Maintains autonomous operation requirements

The implementation prioritizes reliability and clear error reporting over attempting to work around GitHub API issues.