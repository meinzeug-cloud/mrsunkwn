#!/bin/bash

# Unified Agent Sprint - Combines Frontend and Backend Development
echo "🚀 Starting Unified Agent Sprint..."
echo "💻 Working on Backend and Frontend hand in hand..."

export AGENT_ROLE=UNIFIED_AGENT
export GITHUB_TOKEN=${GITHUB_TOKEN:-"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"}
export REPO_OWNER=${REPO_OWNER:-"meinzeug"}
export REPO_NAME=${REPO_NAME:-"mrsunkwn"}

# Check for test mode
TEST_MODE=${TEST_MODE:-false}

# Change to project directory
cd "$(dirname "$0")/.."

# Validate GitHub API connectivity before proceeding
echo "🔍 Validating GitHub API connectivity..."

# Test GitHub API connection
github_test_response=$(curl -s -w "%{http_code}" -o /tmp/github_test.json \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME" 2>/dev/null)

# Check if we got a successful response
if [ "$github_test_response" = "200" ]; then
    echo "✅ GitHub API connectivity verified"
    echo "✅ Repository access confirmed: $REPO_OWNER/$REPO_NAME"
    
    # Export validation flag for the Python script
    export GITHUB_API_VALIDATED=true
    
    # Run the unified sprint
    python3 codex/automation/sprint_runner.py
    
    echo "✅ Unified Agent Sprint complete!"
elif [ "$TEST_MODE" = "true" ]; then
    echo "⚠️ GitHub API connectivity failed, but TEST_MODE is enabled"
    echo "⚠️ Proceeding with local-only development (no GitHub issues will be created)"
    
    # Export test mode flag
    export GITHUB_API_VALIDATED=false
    export TEST_MODE_ENABLED=true
    
    # Run the unified sprint in test mode
    python3 codex/automation/sprint_runner.py
    
    echo "✅ Unified Agent Sprint complete (TEST MODE)!"
else
    echo "❌ GitHub API connectivity failed!"
    echo "❌ HTTP Status Code: $github_test_response"
    
    if [ -f /tmp/github_test.json ]; then
        echo "❌ Response details:"
        cat /tmp/github_test.json
        rm -f /tmp/github_test.json
    fi
    
    echo ""
    echo "🚫 CRITICAL ERROR: GitHub Issues automation is not functional!"
    echo "🚫 Cannot proceed with autonomous issue processing and roadmap execution."
    echo ""
    echo "This could be due to:"
    echo "  1. Invalid or expired GitHub token"
    echo "  2. Network connectivity issues"
    echo "  3. Repository access permissions"
    echo "  4. DNS/proxy blocking GitHub API"
    echo ""
    echo "The autonomous issue processing and GitHub repo updates are required for:"
    echo "  - Planning next development steps"
    echo "  - Processing feature requests"
    echo "  - Coordinating development workflow"
    echo ""
    echo "To run in test mode (local development only), set:"
    echo "  export TEST_MODE=true"
    echo ""
    echo "Otherwise, please fix the GitHub API connectivity before running the agent."
    
    exit 1
fi
