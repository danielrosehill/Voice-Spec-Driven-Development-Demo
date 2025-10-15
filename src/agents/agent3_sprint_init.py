"""Agent 3: Sprint Initialization using Claude Code CLI"""

import os
import subprocess
import tempfile
from pathlib import Path
from ..state import ProjectState, AgentStatus


class SprintInitAgent:
    """
    Agent 3: Executes first development sprint using Claude Code CLI
    Changes to new repository directory and runs Claude Code
    """

    def __init__(self):
        pass

    def create_claude_prompt(self, state: ProjectState) -> str:
        """Create comprehensive prompt for Claude Code CLI"""
        tech_req = state.get("tech_requirements", {})

        prompt = f"""Initialize this project based on the following specification.

PROJECT: {state['project_name']}

DESCRIPTION:
{state['project_description']}

FULL SPECIFICATION:
{state['dev_specification']}

TECHNICAL REQUIREMENTS:
- Languages: {', '.join(tech_req.get('languages', []))}
- Frameworks: {', '.join(tech_req.get('frameworks', []))}
- Dependencies: {', '.join(tech_req.get('dependencies', []))}
- Architecture: {tech_req.get('architecture', 'Not specified')}

FEATURES TO IMPLEMENT:
{chr(10).join(f'{i+1}. {feat}' for i, feat in enumerate(state.get('features', [])))}

TASKS:
1. Analyze the CLAUDE.md file in this repository for full context
2. Set up the project structure based on the technical requirements
3. Initialize package management (requirements.txt, package.json, etc.)
4. Create initial source code files with proper structure
5. Implement core functionality for the main features
6. Add comprehensive README.md with:
   - Project description
   - Installation instructions
   - Usage examples
   - Development setup
7. Set up testing framework with initial tests
8. Create .gitignore file appropriate for the tech stack
9. Add any necessary configuration files
10. Make meaningful commits as you go
11. Ensure the project is in a working, runnable state

IMPORTANT:
- Follow best practices for the chosen tech stack
- Write clean, well-documented code
- Make sure all dependencies are properly specified
- Create a professional, production-ready initial structure
- The project should be immediately usable after this initialization

Begin the development sprint now.
"""
        return prompt

    def execute_claude_code(self, prompt: str, repo_path: str) -> dict:
        """
        Execute Claude Code CLI in the repository directory
        """
        print(f"   Changing directory to: {repo_path}")
        original_cwd = os.getcwd()

        try:
            # Change to repository directory
            os.chdir(repo_path)
            print(f"   ✓ Working directory changed to repository")

            # Create temporary file with prompt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(prompt)
                prompt_file = f.name

            print("   Executing Claude Code CLI...")
            print("   (This may take several minutes as Claude implements the project)")

            # Execute Claude Code CLI
            # Using --print for non-interactive mode and --dangerously-skip-permissions to avoid prompts
            # Read prompt from file
            with open(prompt_file, 'r') as f:
                prompt_content = f.read()

            result = subprocess.run(
                ["claude", "--print", "--dangerously-skip-permissions", prompt_content],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )

            # Clean up prompt file
            os.unlink(prompt_file)

            if result.returncode != 0:
                raise RuntimeError(f"Claude Code failed: {result.stderr}")

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }

        finally:
            # Restore original directory
            os.chdir(original_cwd)

    def get_commit_info(self, repo_path: str) -> dict:
        """Get latest commit information"""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            commit_sha = result.stdout.strip()

            # Get list of files
            result = subprocess.run(
                ["git", "-C", repo_path, "ls-files"],
                capture_output=True,
                text=True,
                check=True
            )
            files = result.stdout.strip().split('\n')

            return {
                "commit_sha": commit_sha,
                "files": files
            }
        except subprocess.CalledProcessError as e:
            return {
                "commit_sha": None,
                "files": []
            }

    def execute(self, state: ProjectState) -> ProjectState:
        """
        Execute Agent 3: Sprint Initialization
        """
        print("🚀 Agent 3: Initializing development sprint with Claude Code...")
        state["current_agent"] = "agent_3_sprint_init"
        state["agent_3_status"] = AgentStatus.IN_PROGRESS

        try:
            # Create Claude prompt
            print("   Creating development prompt...")
            prompt = self.create_claude_prompt(state)

            # Execute Claude Code
            repo_path = state["local_repo_path"]
            result = self.execute_claude_code(prompt, repo_path)

            print("   ✓ Claude Code execution completed")

            # Get commit information
            commit_info = self.get_commit_info(repo_path)
            state["initial_commit_sha"] = commit_info["commit_sha"]
            state["files_created"] = commit_info["files"]

            print(f"   ✓ Latest commit: {commit_info['commit_sha'][:8]}")
            print(f"   ✓ Files created: {len(commit_info['files'])}")

            # Check if dependencies were installed
            # This is a heuristic - check for common dependency files
            dependency_files = [
                "requirements.txt", "package.json", "Cargo.toml",
                "go.mod", "pom.xml", "Gemfile"
            ]
            has_deps = any(
                dep_file in commit_info["files"]
                for dep_file in dependency_files
            )
            state["dependencies_installed"] = has_deps

            state["agent_3_status"] = AgentStatus.COMPLETED

            # Create success message
            state["success_message"] = f"""
✅ Project initialized successfully!

📍 Local: {state['local_repo_path']}
🌐 Remote: {state['repo_url']}

The project has been fully set up and is ready for development.
"""
            state["completed"] = True

        except subprocess.TimeoutExpired:
            state["agent_3_status"] = AgentStatus.FAILED
            state["errors"].append("Agent 3 timeout: Claude Code took too long")
            print("   ✗ Error: Execution timeout")
            raise

        except Exception as e:
            state["agent_3_status"] = AgentStatus.FAILED
            state["errors"].append(f"Agent 3 failed: {str(e)}")
            print(f"   ✗ Error: {str(e)}")
            raise

        return state


def agent3_node(state: ProjectState) -> ProjectState:
    """LangGraph node for Agent 3"""
    agent = SprintInitAgent()
    return agent.execute(state)
