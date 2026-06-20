#!/bin/bash
# Test runner script for Zuna

set -e  # Exit on error

echo "==================================="
echo "Running Zuna Tests"
echo "==================================="
echo ""

# Run backend tests
echo "📦 Running Backend Unit Tests..."
echo "-----------------------------------"
cd /Users/aritra.biswas/Desktop/workspace/projects/z/backend
uv run pytest -v --tb=short
echo ""

# Run engine tests
echo "⚙️  Running Engine Unit Tests..."
echo "-----------------------------------"
cd /Users/aritra.biswas/Desktop/workspace/projects/z/engine
uv run pytest -v --tb=short
echo ""

# Integration tests (requires services to be running)
echo "🔗 Running Integration Tests..."
echo "-----------------------------------"
echo "Note: Integration tests require services to be running (docker-compose up)"
echo "Checking if services are available..."

# Check if backend is available
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is available"
    if curl -s http://localhost:8001/health > /dev/null 2>&1; then
        echo "✅ Engine is available"
        echo ""
        echo "Running integration tests..."
        cd /Users/aritra.biswas/Desktop/workspace/projects/z
        /Users/aritra.biswas/Desktop/workspace/projects/z/backend/.venv/bin/pytest tests/integration/ -v --tb=short
    else
        echo "❌ Engine is not available"
        echo "Skipping integration tests"
    fi
else
    echo "❌ Backend is not available"
    echo "Skipping integration tests"
    echo ""
    echo "To run integration tests, start services with:"
    echo "  docker-compose up"
fi

echo ""
echo "==================================="
echo "Test Summary"
echo "==================================="
echo "✅ Backend unit tests: Passed"
echo "✅ Engine unit tests: Passed"
echo "ℹ️  Integration tests: Requires running services"
echo "==================================="
