# Three-Agent Workflow Documentation

## Overview

This document describes the Voice-Spec-Driven Development multi-agent workflow, which transforms audio recordings of software specifications into fully initialized development projects with active development sprints.

## Workflow Goal

**Primary Objective**: Enable developers to voice-record software specifications and automatically generate a working GitHub repository with project initialization and first development sprint kickoff.

**Success Criteria**: User receives a message stating "The project has been kicked off here: {local_path} | {GitHub_repo_URL}" after the workflow completes.

## Architecture Overview

The workflow consists of three sequential agents that operate locally (POC CLI, potential lightweight GUI) but integrate with cloud LLM APIs for processing.

**Important Note**: This is not a local AI system. It runs locally but leverages cloud-based LLM APIs (Gemini, Claude, etc.) for AI processing.

---

## Agent 1: Transcription and Prompt Optimization Agent

### Technology
- **LLM**: Gemini (Google Cloud API)

### Role
Transform raw audio specifications into optimized development prompts suitable for project initialization.

### Input
- Audio recording of software specification (voice memo, meeting recording, etc.)

### Responsibilities
1. **Transcribe**: Convert audio to text using Gemini's transcription capabilities
2. **Parse**: Extract key project requirements, features, and constraints
3. **Structure**: Organize information into a coherent development specification
4. **Optimize**: Refine the prompt for clarity and actionability
5. **Format**: Output a developer-friendly specification document

### Output
- Structured development prompt/specification
- Project metadata (name, description, key features)
- Technical requirements identified from the audio

### Success Metrics
- Accurate transcription of audio content
- Coherent and actionable development specification
- Properly extracted project metadata

---

## Agent 2: Repository Creation Agent

### Technology
- **Tool**: GitHub CLI (`gh`)
- **Alternative**: GitHub MCP (future consideration)

### Role
Initialize a new GitHub repository with proper structure and configuration.

### Input
- Development prompt/specification from Agent 1
- Project metadata (name, description)

### Responsibilities
1. **Create Repository**: Use `gh` CLI to create a new GitHub repository
2. **Initialize Structure**: Set up basic project structure
3. **Generate CLAUDE.md**: Create project-specific instructions for Claude Code
4. **Configure Settings**: Set repository visibility, branch protection, etc.
5. **Local Clone**: Clone repository to local development environment

### Output
- GitHub repository (remote)
- Local repository clone
- CLAUDE.md file with project context
- Repository URL and local path

### Critical Transition Point
**Change of Working Directory (CWD)**: After this agent completes, the workflow transitions from the framework's directory to the newly created repository directory. All subsequent operations occur within the new project context.

### Success Metrics
- GitHub repository successfully created
- CLAUDE.md file present in repository
- Local clone successful
- CWD transition handled correctly

---

## Agent 3: Sprint Initialization Agent

### Technology
- **LLM**: Claude (via Claude Code CLI)

### Role
Execute the first development sprint to establish project foundation and working codebase.

### Input
- Development specification from Agent 1
- Repository context (CLAUDE.md, project structure)
- Local repository path

### Responsibilities
1. **Project Setup**: Initialize project dependencies and build tools
2. **Scaffold**: Create initial codebase structure
3. **Implement Core**: Build foundational features
4. **Documentation**: Create README, contributing guides, etc.
5. **Testing**: Set up testing framework and initial tests
6. **Commit**: Make initial commits with meaningful messages
7. **Push**: Synchronize with GitHub remote

### Output
- Working initial codebase
- Project documentation
- First commit(s) pushed to GitHub
- Development environment ready for continued work

### Success Metrics
- Runnable/buildable project
- Proper project structure established
- Documentation present
- Clean git history
- Remote repository synchronized

---

## Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│ User Records Audio Specification                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 1: Transcription & Optimization (Gemini)              │
│                                                              │
│ Input:  Audio file                                          │
│ Output: Structured development specification                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 2: Repository Creation (GitHub CLI)                   │
│                                                              │
│ Input:  Development specification                           │
│ Output: GitHub repo + local clone + CLAUDE.md              │
│                                                              │
│ ⚠️  CWD TRANSITION: Framework dir → New project dir        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ AGENT 3: Sprint Initialization (Claude Code CLI)            │
│                                                              │
│ Input:  Specification + repo context                        │
│ Output: Working codebase + documentation + commits          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ SUCCESS MESSAGE                                              │
│                                                              │
│ "The project has been kicked off here:                      │
│  Local: /path/to/repo                                       │
│  Remote: https://github.com/user/repo"                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Considerations

### Working Directory Management
- **Agent 1**: Operates in framework directory
- **Agent 2**: Operates in framework directory, creates new directory
- **Agent 3**: Operates in newly created project directory
- **Transition Logic**: Must handle CWD change between Agent 2 and Agent 3

### API Integration
- **Gemini API**: Transcription and prompt optimization
- **GitHub API**: Repository creation (via `gh` CLI)
- **Claude API**: Development sprint (via Claude Code CLI)

### Error Handling
Each agent should handle failures gracefully:
- **Agent 1**: Audio transcription errors, invalid audio format
- **Agent 2**: Repository name conflicts, authentication issues
- **Agent 3**: Build failures, dependency issues

### State Management
- Pass project context between agents
- Maintain metadata throughout workflow
- Track completion status of each agent

---

## Future Enhancements

1. **GUI Interface**: Migrate from CLI to lightweight GUI
2. **GitHub MCP**: Replace `gh` CLI with GitHub MCP integration
3. **Multi-LLM Support**: Allow user selection of LLMs for each agent
4. **Workflow Customization**: Configurable agent behavior
5. **Resume Capability**: Handle interruptions and resume workflow
6. **Template System**: Pre-defined project templates for common types

---

## Framework Selection

The implementation should leverage existing multi-agent frameworks rather than building from scratch. Suitable frameworks should support:
- Sequential agent execution
- Context passing between agents
- External API integration
- Working directory management
- Error handling and recovery

Refer to framework evaluation documentation for specific recommendations.
