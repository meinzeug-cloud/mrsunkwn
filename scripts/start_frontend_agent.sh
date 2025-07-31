#!/bin/bash

# Start Frontend Agent Sprint
echo "🎨 Starting Frontend Agent Sprint..."

export AGENT_ROLE=FRONTEND_AGENT
export GITHUB_TOKEN=${GITHUB_TOKEN:-"your_github_token_here"}
export REPO_OWNER=${REPO_OWNER:-"meinzeug"}
export REPO_NAME=${REPO_NAME:-"mrsunkwn"}

# Change to project directory
cd "$(dirname "$0")/.."

# Run the sprint
python3 codex/automation/sprint_runner.py

echo "✅ Frontend Agent Sprint complete!"