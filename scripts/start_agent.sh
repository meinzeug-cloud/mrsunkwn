#!/bin/bash

# Unified Agent Sprint - Combines Frontend and Backend Development
echo "🚀 Starting Unified Agent Sprint..."
echo "💻 Working on Backend and Frontend hand in hand..."

export AGENT_ROLE=UNIFIED_AGENT
export GITHUB_TOKEN=${GITHUB_TOKEN:-"your_github_token_here"}
export REPO_OWNER=${REPO_OWNER:-"meinzeug"}
export REPO_NAME=${REPO_NAME:-"mrsunkwn"}

# Change to project directory
cd "$(dirname "$0")/.."

# Run the unified sprint
python3 codex/automation/sprint_runner.py

echo "✅ Unified Agent Sprint complete!"