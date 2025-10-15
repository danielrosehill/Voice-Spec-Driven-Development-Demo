"""Agent 1: Audio Transcription and Specification Optimization using Gemini"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from ..state import ProjectState, AgentStatus


class TechRequirements(BaseModel):
    """Technical requirements schema"""
    languages: List[str] = Field(description="List of programming languages")
    frameworks: List[str] = Field(description="List of frameworks and libraries")
    dependencies: List[str] = Field(description="List of dependencies")
    architecture: str = Field(description="Architecture description")


class ProjectSpecification(BaseModel):
    """Structured project specification schema"""
    project_name: str = Field(description="Suggested project name in kebab-case")
    project_description: str = Field(description="Brief 1-2 sentence description")
    dev_specification: str = Field(description="Detailed specification in markdown format")
    tech_requirements: TechRequirements = Field(description="Technical requirements")
    features: List[str] = Field(description="List of features and functionalities")


class TranscriptionAgent:
    """
    Agent 1: Transcribes audio and optimizes it into a development specification
    Uses Gemini API for audio transcription and prompt optimization
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash-exp"

    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file using Gemini"""
        audio_file = Path(audio_file_path)
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        # Upload audio file using new API
        uploaded_file = self.client.files.upload(file=audio_file_path)

        # Transcribe using multimodal input
        prompt = """
        Please transcribe this audio recording accurately.
        This is a software specification being dictated by a developer.
        Include all technical details, feature requirements, and constraints mentioned.
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[prompt, uploaded_file]
        )
        return response.text

    def optimize_specification(self, transcript: str) -> Dict[str, Any]:
        """
        Parse transcript and create structured development specification using structured output
        """
        prompt = f"""
        You are a technical specification analyst. Parse the following transcript
        of a software project specification and extract structured information.

        Transcript:
        {transcript}

        Guidelines:
        - Suggest a clear, kebab-case project name
        - Create a comprehensive specification that Claude Code can use
        - Identify all technical requirements mentioned or implied
        - List all features and functionalities
        - If information is unclear, make reasonable technical decisions
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=ProjectSpecification,
            )
        )

        # Parse the structured response - response.text is guaranteed valid JSON
        spec_data = json.loads(response.text)
        return spec_data

    def execute(self, state: ProjectState) -> ProjectState:
        """
        Execute Agent 1: Transcription and Optimization
        """
        print("🎤 Agent 1: Starting audio transcription and specification optimization...")
        state["current_agent"] = "agent_1_transcription"
        state["agent_1_status"] = AgentStatus.IN_PROGRESS

        try:
            # Transcribe audio
            print(f"   Transcribing audio from: {state['audio_file_path']}")
            transcript = self.transcribe_audio(state["audio_file_path"])
            state["transcript"] = transcript
            print(f"   ✓ Transcription complete ({len(transcript)} characters)")

            # Optimize specification
            print("   Optimizing specification...")
            spec_data = self.optimize_specification(transcript)

            # Update state
            state["project_name"] = spec_data["project_name"]
            state["project_description"] = spec_data["project_description"]
            state["dev_specification"] = spec_data["dev_specification"]
            state["tech_requirements"] = spec_data["tech_requirements"]
            state["features"] = spec_data["features"]

            state["agent_1_status"] = AgentStatus.COMPLETED
            print(f"   ✓ Specification optimized for project: {spec_data['project_name']}")
            print(f"   ✓ Identified {len(spec_data['features'])} features")

        except Exception as e:
            state["agent_1_status"] = AgentStatus.FAILED
            state["errors"].append(f"Agent 1 failed: {str(e)}")
            print(f"   ✗ Error: {str(e)}")
            raise

        return state


def agent1_node(state: ProjectState) -> ProjectState:
    """LangGraph node for Agent 1"""
    agent = TranscriptionAgent()
    return agent.execute(state)
