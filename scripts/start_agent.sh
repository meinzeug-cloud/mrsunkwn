#!/bin/bash

# Unified Agent Sprint - Combines Frontend and Backend Development
echo "🚀 Starting Unified Agent Sprint..."
echo "💻 Working on Backend and Frontend hand in hand..."

export AGENT_ROLE=UNIFIED_AGENT
export GITHUB_TOKEN=${GITHUB_TOKEN:-"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"}
export REPO_OWNER=${REPO_OWNER:-"meinzeug"}
export REPO_NAME=${REPO_NAME:-"mrsunkwn"}

# Change to project directory
cd "$(dirname "$0")/.."

# Run the unified sprint
python3 codex/automation/sprint_runner.py

echo "✅ Unified Agent Sprint complete!"
