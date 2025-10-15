#!/bin/bash
# Setup script for Voice-Spec-Driven Development
# Uses uv for fast Python package management

set -e

echo "🚀 Voice-Spec-Driven Development - Setup"
echo "=========================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo ""
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo ""
    echo "✓ uv installed"
    echo ""
    echo "⚠️  Please restart your shell and run this script again"
    exit 0
fi

echo "✓ uv is installed"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment with uv
echo "Creating virtual environment with uv..."
uv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies with uv
echo "Installing dependencies with uv..."
uv pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found"
    echo "   Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "📝 Please edit .env and add your API keys:"
    echo "   - GEMINI_API_KEY"
    echo "   - GITHUB_TOKEN"
    echo ""
else
    echo "✓ .env file exists"
    echo ""
fi

# Check for Node.js and npx (needed for GitHub MCP)
if ! command -v npx &> /dev/null; then
    echo "⚠️  npx is not installed (required for GitHub MCP)"
    echo "   Please install Node.js: https://nodejs.org/"
    echo ""
else
    echo "✓ npx is installed"
    echo ""
fi

# Check for Claude CLI
if ! command -v claude &> /dev/null; then
    echo "⚠️  Claude CLI is not installed (required for Agent 3)"
    echo "   Install: npm install -g @anthropics/claude-code"
    echo ""
else
    echo "✓ Claude CLI is installed"
    echo ""
fi

# Make CLI executable
chmod +x src/cli.py

echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Configure your API keys in .env"
echo ""
echo "  3. Check your environment:"
echo "     python -m src.cli check"
echo ""
echo "  4. Run the workflow:"
echo "     python -m src.cli run /path/to/audio/file.mp3"
echo ""
echo "For more information, see README.md"
echo ""
