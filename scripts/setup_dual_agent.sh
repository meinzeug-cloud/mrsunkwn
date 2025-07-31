#!/bin/bash

# Setup Dual-Agent System
echo "🚀 Setting up Dual-Agent System..."

# Set environment variables
export AGENT_ROLE=SETUP_AGENT
export GITHUB_TOKEN=${GITHUB_TOKEN:-"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"}
export REPO_OWNER=${REPO_OWNER:-"meinzeug"}
export REPO_NAME=${REPO_NAME:-"mrsunkwn"}

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p frontend/src/{components,hooks,services}
mkdir -p backend/src
mkdir -p codex/{automation,data/{frontend,backend,shared}}

echo "✅ Dual-Agent System setup complete!"
echo ""
echo "Next steps:"
echo "1. Set GITHUB_TOKEN environment variable"
echo "2. Run: ./scripts/start_frontend_agent.sh"
echo "3. Run: ./scripts/start_backend_agent.sh"
