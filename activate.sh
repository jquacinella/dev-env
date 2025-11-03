#!/bin/bash

# Activation helper for dev-env virtual environment

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

VENV_DIR=".venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠${NC} Virtual environment not found at $VENV_DIR"
    echo -e "${BLUE}ℹ${NC} Run ./setup.sh first to create the environment"
    return 1 2>/dev/null || exit 1
fi

# Check if already activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${YELLOW}⚠${NC} A virtual environment is already active: $VIRTUAL_ENV"
    echo -e "${BLUE}ℹ${NC} Deactivate it first with: deactivate"
    return 1 2>/dev/null || exit 1
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

echo -e "${GREEN}✓${NC} Virtual environment activated!"
echo ""
echo -e "${BLUE}Available commands:${NC}"
echo "  ansible-playbook dev-setup.yml --ask-become-pass  # Run full setup"
echo "  ansible-playbook dev-setup.yml --tags fzf         # Install specific tool"
echo "  ansible-playbook version-checks.yml               # Check for updates"
echo "  deactivate                                        # Exit virtual environment"
echo ""
