#!/bin/bash

# Demonstration of the Dual-Agent System
echo "🚀 Dual-Agent System Demonstration"
echo "===================================="

# Set environment variables
export GITHUB_TOKEN=${GITHUB_TOKEN:-"your_github_token_here"}
export REPO_OWNER=${REPO_OWNER:-"meinzeug"}
export REPO_NAME=${REPO_NAME:-"mrsunkwn"}

echo ""
echo "🎨 Running Frontend Agent Sprint..."
echo "-----------------------------------"
export AGENT_ROLE=FRONTEND_AGENT
python3 codex/automation/sprint_runner.py

echo ""
echo "⚡ Running Backend Agent Sprint..."
echo "---------------------------------"
export AGENT_ROLE=BACKEND_AGENT
python3 codex/automation/sprint_runner.py

echo ""
echo "🧪 Testing Backend API..."
echo "-------------------------"
echo "Starting backend server in background..."
cd backend
python3 src/app.py &
BACKEND_PID=$!
cd ..

# Wait for server to start
sleep 3

echo "Testing /api/status endpoint:"
curl -s http://localhost:8000/api/status | python3 -m json.tool

echo ""
echo "Testing /api/data endpoint:"
curl -s http://localhost:8000/api/data | python3 -m json.tool

# Clean up
echo ""
echo "🧹 Cleaning up..."
kill $BACKEND_PID 2>/dev/null

echo ""
echo "✅ Demonstration Complete!"
echo ""
echo "📊 Generated Files:"
find frontend/src/components -name "*.tsx" 2>/dev/null | head -5
echo ""
echo "📋 See DUAL_AGENT_SETUP.md for detailed usage instructions."