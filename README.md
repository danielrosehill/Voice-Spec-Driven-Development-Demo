# Voice Spec-Driven Development

A 3-agent AI system powered by LangGraph that transforms voice recordings into working applications: Voice → Spec → Repo → Development.

## Overview

Record your software ideas as audio, and the system autonomously:
1. **Transcribes** and optimizes into development specifications (Gemini)
2. **Creates** GitHub repositories with project context (GitHub MCP)
3. **Develops** the application to working state (Claude Code CLI)

## Multi-Agent Architecture (LangGraph)

Built on **LangGraph**, a framework for stateful multi-agent workflows:

### Agent 1: Transcription & Optimization
- **LLM**: Google Gemini 2.0 Flash
- **Purpose**: Audio → Structured development specification
- **Output**: Project metadata, tech requirements, feature list

### Agent 2: Repository Creation
- **Tool**: GitHub MCP (Model Context Protocol)
- **Purpose**: Create and initialize GitHub repository
- **Output**: GitHub repo, CLAUDE.md, local clone

### Agent 3: Sprint Initialization
- **Tool**: Claude Code CLI
- **Purpose**: First development sprint
- **Output**: Working codebase, tests, documentation

## Features

- **LangGraph Orchestration**: State-based workflow with error handling
- **GitHub MCP Integration**: Modern API-native GitHub interactions
- **Conditional Routing**: Smart decision-making between agents
- **State Persistence**: Track progress through entire workflow
- **Error Recovery**: Graceful failure handling at each stage
- **Type-Safe State**: Strongly typed state management

## Directory Structure

```
Voice-Spec-Driven-Development-Demo/
├── src/
│   ├── __init__.py
│   ├── state.py                 # LangGraph state schema
│   ├── workflow.py              # LangGraph workflow definition
│   ├── cli.py                   # CLI entry point
│   └── agents/
│       ├── __init__.py
│       ├── agent1_transcription.py
│       ├── agent2_repo_creation.py
│       └── agent3_sprint_init.py
├── docs/                        # Documentation
├── requirements.txt             # Python dependencies
├── setup.sh                     # Setup script (uses uv)
├── .env.example                 # Environment template
└── README.md
```

## Setup

### Quick Setup (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd Voice-Spec-Driven-Development-Demo

# Run setup script (installs uv if needed)
bash setup.sh

# Activate virtual environment
source .venv/bin/activate

# Configure API keys in .env
# Edit GEMINI_API_KEY and GITHUB_TOKEN
```

### Manual Setup

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Prerequisites

- Python 3.10+
- Node.js and npm (for GitHub MCP)
- Claude Code CLI: `npm install -g @anthropics/claude-code`
- GitHub Personal Access Token with `repo` scope
- Google Gemini API Key

### API Keys

1. **Gemini API Key**: https://makersuite.google.com/app/apikey
2. **GitHub Token**: https://github.com/settings/tokens (scopes: `repo`, `workflow`)

## Usage

### Interactive Mode (Recommended)

Simply run the script to see a menu of available audio files:

```bash
./run.sh
```

This will:
1. Show a table of all audio files in `audio/to-process/`
2. Let you select which file to process
3. Run the complete 3-agent workflow
4. Move processed file to `audio/processed/`

**Example interaction:**
```
┌──────┬────────────────────┬─────────┬──────────────────┐
│  #   │ Filename           │ Size    │ Modified         │
├──────┼────────────────────┼─────────┼──────────────────┤
│  1   │ app-idea.mp3       │ 2.4 MB  │ 2025-10-15 14:30 │
│  2   │ feature-spec.wav   │ 1.8 MB  │ 2025-10-14 09:15 │
└──────┴────────────────────┴─────────┴──────────────────┘

Select audio file number (or 'q' to quit) [1]: 1
```

### Direct File Mode

Process a specific audio file directly:

```bash
./run.sh run /path/to/audio/file.mp3
```

### Check Environment

Verify your setup:

```bash
./run.sh check
```

Verifies:
- Environment variables set
- Claude CLI installed
- GitHub MCP accessible

### Workflow Steps

The complete workflow executes:
1. Agent 1 transcribes audio and creates specification
2. Agent 2 creates GitHub repository and CLAUDE.md
3. Agent 3 develops the application with Claude Code CLI

### Example Output

```
🎤 Agent 1: Starting audio transcription...
   ✓ Transcription complete (1543 characters)
   ✓ Specification optimized for project: my-awesome-app
   ✓ Identified 5 features

📦 Agent 2: Creating GitHub repository...
   ✓ Repository created: https://github.com/user/my-awesome-app
   ✓ CLAUDE.md created in repository
   ✓ Repository cloned to: ~/repos/github/my-awesome-app

🚀 Agent 3: Initializing development sprint...
   ✓ Claude Code execution completed
   ✓ Latest commit: a1b2c3d4
   ✓ Files created: 15

✅ Project initialized successfully!

📍 Local: /home/user/repos/github/my-awesome-app
🌐 Remote: https://github.com/user/my-awesome-app
```

## LangGraph Workflow

```
START
  ↓
[Agent 1: Transcription]
  ↓
[Success?] → [Error Handler]
  ↓
[Agent 2: Repo Creation]
  ↓
[Success?] → [Error Handler]
  ↓
[Agent 3: Sprint Init]
  ↓
[Success?] → [Error Handler]
  ↓
END
```

## State Management

The workflow maintains state through all agents:

```python
ProjectState:
  - audio_file_path
  - transcript
  - project_name
  - dev_specification
  - tech_requirements
  - repo_url
  - local_repo_path
  - files_created
  - completed
  - errors
```

## Supported Audio Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- M4A (`.m4a`)
- OGG (`.ogg`)
- FLAC (`.flac`)

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

## Architecture Highlights

- **LangGraph**: Production-ready multi-agent orchestration
- **GitHub MCP**: Modern protocol for GitHub API interactions
- **Type Safety**: Pydantic models for state validation
- **Error Handling**: Graceful failures with detailed error tracking
- **CLI Interface**: Rich terminal UI with progress indicators

## Troubleshooting

### Environment Check Failed
```bash
python -m src.cli check
```
Review which components are missing or misconfigured.

### GitHub MCP Connection Issues
Ensure `GITHUB_TOKEN` has correct scopes and is valid.

### Claude CLI Not Found
```bash
npm install -g @anthropics/claude-code
```

## Documentation

See `docs/` folder for:
- `three-agent-workflow.md`: Original workflow design
- `langgraph-architecture.md`: LangGraph implementation details
- `github-mcp-integration.md`: GitHub MCP integration guide

 