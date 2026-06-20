#!/usr/bin/env bash

# Setup script for pre-commit hooks
# This script initializes the pre-commit environment

set -e

echo "=================================="
echo "Pre-Commit Hooks Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the project root
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: Must run from project root${NC}"
    exit 1
fi

# Step 1: Check/create venv
echo "Step 1: Checking Python virtual environment..."
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment with Python 3.12...${NC}"
    uv venv --python 3.12
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

# Step 2: Activate venv and install dependencies
echo ""
echo "Step 2: Installing dependencies..."
source .venv/bin/activate

# Install pre-commit, ruff, and bandit
uv pip install pre-commit ruff "bandit[toml]"
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 3: Install git hooks
echo ""
echo "Step 3: Installing git hooks..."
pre-commit install
pre-commit install --hook-type commit-msg
echo -e "${GREEN}✓ Git hooks installed${NC}"

# Step 4: Run hooks on all files (optional)
echo ""
echo "Step 4: Testing hooks (optional)..."
read -p "Run pre-commit on all files now? This may take a few minutes. (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Running pre-commit on all files...${NC}"
    pre-commit run --all-files || true
    echo -e "${GREEN}✓ Pre-commit test complete${NC}"
else
    echo "Skipped. You can run it later with: pre-commit run --all-files"
fi

# Success message
echo ""
echo "=================================="
echo -e "${GREEN}✓ Pre-commit setup complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate venv: source .venv/bin/activate"
echo "2. Read docs: cat PRE_COMMIT_SETUP.md"
echo "3. Test hooks: pre-commit run --all-files"
echo "4. Make a commit: git commit -m 'your message'"
echo ""
echo "Hooks will run automatically on each commit!"
