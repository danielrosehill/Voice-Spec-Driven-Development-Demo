"""LangGraph State Schema for Voice-Spec-Driven Development Workflow"""

from typing import TypedDict, Optional, List, Dict, Any
from enum import Enum


class AgentStatus(str, Enum):
    """Agent execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectState(TypedDict, total=False):
    """
    State object that flows through the LangGraph workflow.
    Contains all data needed by agents and passed between nodes.
    """

    # Input
    audio_file_path: str

    # Agent 1: Transcription & Optimization (Gemini)
    transcript: Optional[str]
    project_name: Optional[str]
    project_description: Optional[str]
    dev_specification: Optional[str]
    tech_requirements: Optional[Dict[str, Any]]
    features: Optional[List[str]]

    # Agent 2: Repository Creation (GitHub MCP)
    repo_url: Optional[str]
    repo_owner: Optional[str]
    local_repo_path: Optional[str]
    claude_md_content: Optional[str]
    initial_files_created: Optional[List[str]]

    # Agent 3: Sprint Initialization (Claude Code CLI)
    initial_commit_sha: Optional[str]
    files_created: Optional[List[str]]
    dependencies_installed: Optional[bool]
    tests_passing: Optional[bool]

    # Workflow Control
    current_agent: str
    agent_1_status: AgentStatus
    agent_2_status: AgentStatus
    agent_3_status: AgentStatus

    # Error Handling
    errors: List[str]
    warnings: List[str]

    # Completion
    completed: bool
    success_message: Optional[str]


def create_initial_state(audio_file_path: str) -> ProjectState:
    """Create initial state for workflow execution"""
    return ProjectState(
        audio_file_path=audio_file_path,
        current_agent="start",
        agent_1_status=AgentStatus.PENDING,
        agent_2_status=AgentStatus.PENDING,
        agent_3_status=AgentStatus.PENDING,
        errors=[],
        warnings=[],
        completed=False,
    )
