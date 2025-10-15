#!/bin/bash
# Run Voice-Spec-Driven Development CLI

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found"
    echo ""
    echo "Please run setup first:"
    echo "  bash setup.sh"
    echo ""
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Run CLI with all arguments passed through
if [ $# -eq 0 ]; then
    # No arguments - run interactive mode
    python -m src.cli
else
    # Pass all arguments to CLI
    python -m src.cli "$@"
fi
