#!/usr/bin/env python3
"""CLI Entry Point for Voice-Spec-Driven Development"""

import os
import sys
import shutil
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from dotenv import load_dotenv

from .state import create_initial_state
from .workflow import compile_workflow

# Load environment variables
load_dotenv()

console = Console()

# Audio processing directories
AUDIO_TO_PROCESS = Path(__file__).parent.parent / "spec" / "audio" / "to-process"
AUDIO_PROCESSED = Path(__file__).parent.parent / "spec" / "audio" / "processed"

# Supported audio formats
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm'}


def validate_environment():
    """Validate required environment variables"""
    required_vars = {
        "GEMINI_API_KEY": "Google Gemini API key",
        "GITHUB_TOKEN": "GitHub Personal Access Token"
    }

    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"  • {var}: {description}")

    if missing:
        console.print("\n[red]❌ Missing required environment variables:[/red]")
        for item in missing:
            console.print(item)
        console.print("\n[yellow]Please set these in your .env file or environment.[/yellow]")
        console.print("See .env.example for reference.\n")
        sys.exit(1)


def get_audio_files():
    """Get list of audio files in to-process directory"""
    if not AUDIO_TO_PROCESS.exists():
        AUDIO_TO_PROCESS.mkdir(parents=True, exist_ok=True)

    audio_files = []
    for file in AUDIO_TO_PROCESS.iterdir():
        if file.is_file() and file.suffix.lower() in AUDIO_EXTENSIONS:
            audio_files.append(file)

    return sorted(audio_files, key=lambda f: f.stat().st_mtime, reverse=True)


def display_audio_menu():
    """Display interactive menu of audio files"""
    audio_files = get_audio_files()

    if not audio_files:
        console.print("\n[yellow]No audio files found in audio/to-process/[/yellow]")
        console.print(f"\n[dim]Please add audio files to: {AUDIO_TO_PROCESS}[/dim]")
        console.print(f"[dim]Supported formats: {', '.join(AUDIO_EXTENSIONS)}[/dim]\n")
        return None

    # Create table
    table = Table(title="Available Audio Files", show_header=True, header_style="bold cyan")
    table.add_column("#", style="cyan", width=6)
    table.add_column("Filename", style="white")
    table.add_column("Size", style="yellow", justify="right")
    table.add_column("Modified", style="dim")

    for idx, file in enumerate(audio_files, 1):
        size = file.stat().st_size
        size_str = f"{size / 1024:.1f} KB" if size < 1024 * 1024 else f"{size / (1024 * 1024):.1f} MB"
        modified = file.stat().st_mtime
        from datetime import datetime
        modified_str = datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M")

        table.add_row(str(idx), file.name, size_str, modified_str)

    console.print()
    console.print(table)
    console.print()

    # Prompt for selection
    while True:
        choice = Prompt.ask(
            "[cyan]Select audio file number[/cyan] (or 'q' to quit)",
            default="1"
        )

        if choice.lower() == 'q':
            return None

        try:
            idx = int(choice)
            if 1 <= idx <= len(audio_files):
                return audio_files[idx - 1]
            else:
                console.print(f"[red]Invalid selection. Please choose 1-{len(audio_files)}[/red]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a number or 'q' to quit[/red]")


def move_to_processed(audio_file: Path):
    """Move processed audio file to processed directory"""
    if not AUDIO_PROCESSED.exists():
        AUDIO_PROCESSED.mkdir(parents=True, exist_ok=True)

    destination = AUDIO_PROCESSED / audio_file.name

    # Handle name conflicts
    counter = 1
    while destination.exists():
        stem = audio_file.stem
        suffix = audio_file.suffix
        destination = AUDIO_PROCESSED / f"{stem}_{counter}{suffix}"
        counter += 1

    shutil.move(str(audio_file), str(destination))
    return destination


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Voice-Spec-Driven Development - Transform audio specs into working projects"""
    if ctx.invoked_subcommand is None:
        # No subcommand provided, run interactive mode
        run_interactive()


def run_interactive():
    """Run interactive mode - select audio file from menu"""
    # Validate environment
    validate_environment()

    # Display banner
    console.print(Panel.fit(
        "[bold cyan]Voice-Spec-Driven Development[/bold cyan]\n"
        "Audio → Specification → Repository → Development",
        border_style="cyan"
    ))

    # Display audio file menu
    selected_file = display_audio_menu()

    if selected_file is None:
        console.print("[yellow]No file selected. Exiting.[/yellow]\n")
        sys.exit(0)

    # Run workflow with selected file
    run_workflow(selected_file)


def run_workflow(audio_path: Path):
    """Execute the workflow with given audio file"""
    console.print(f"\n📁 Processing: [cyan]{audio_path.name}[/cyan]\n")

    # Create initial state
    initial_state = create_initial_state(str(audio_path))

    # Compile workflow
    console.print("[cyan]🔧 Compiling LangGraph workflow...[/cyan]")
    app = compile_workflow()
    console.print("[green]✓ Workflow compiled[/green]\n")

    # Run workflow
    console.print("[bold]Starting 3-agent workflow...[/bold]\n")

    try:
        final_state = app.invoke(initial_state)

        # Display results
        if final_state["completed"]:
            console.print(Panel(
                final_state["success_message"],
                title="[bold green]✅ Success[/bold green]",
                border_style="green"
            ))

            # Display project details
            console.print("\n[bold]Project Details:[/bold]")
            console.print(f"  Name: {final_state['project_name']}")
            console.print(f"  Description: {final_state['project_description']}")
            console.print(f"  Features: {len(final_state.get('features', []))}")
            console.print(f"  Files Created: {len(final_state.get('files_created', []))}")
            console.print()

            # Move processed file
            processed_path = move_to_processed(audio_path)
            console.print(f"[dim]✓ Moved audio file to: {processed_path}[/dim]\n")

        else:
            console.print(Panel(
                "[red]Workflow completed with errors[/red]\n\n"
                f"Errors:\n" + "\n".join(f"  • {e}" for e in final_state['errors']),
                title="[bold red]❌ Failed[/bold red]",
                border_style="red"
            ))
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Workflow interrupted by user[/yellow]\n")
        sys.exit(130)

    except Exception as e:
        console.print(f"\n[red]❌ Workflow failed with error:[/red]\n{str(e)}\n")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@cli.command()
@click.argument('audio_file', type=click.Path(exists=True), required=False)
def run(audio_file: str = None):
    """
    Run the complete workflow with an audio specification file

    If AUDIO_FILE is not provided, shows interactive menu of files in audio/to-process/
    """
    # Validate environment
    validate_environment()

    if audio_file:
        # Direct mode - file path provided
        audio_path = Path(audio_file).resolve()
        if not audio_path.exists():
            console.print(f"\n[red]❌ Audio file not found: {audio_file}[/red]\n")
            sys.exit(1)

        # Display banner
        console.print(Panel.fit(
            "[bold cyan]Voice-Spec-Driven Development[/bold cyan]\n"
            "Audio → Specification → Repository → Development",
            border_style="cyan"
        ))

        run_workflow(audio_path)
    else:
        # Interactive mode - show menu
        run_interactive()


@cli.command()
def check():
    """Check environment setup and dependencies"""
    console.print("\n[cyan]Checking environment...[/cyan]\n")

    # Check Python version
    py_version = sys.version_info
    console.print(f"Python: {py_version.major}.{py_version.minor}.{py_version.micro}")

    # Check environment variables
    env_vars = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")
    }

    console.print("\nEnvironment Variables:")
    for var, value in env_vars.items():
        status = "✓" if value else "✗"
        color = "green" if value else "red"
        masked = f"{value[:8]}..." if value else "Not set"
        console.print(f"  [{color}]{status}[/{color}] {var}: {masked}")

    # Check Claude CLI
    try:
        import subprocess
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        claude_version = result.stdout.strip() if result.returncode == 0 else "Not found"
        status = "✓" if result.returncode == 0 else "✗"
        color = "green" if result.returncode == 0 else "red"
        console.print(f"\nClaude CLI:")
        console.print(f"  [{color}]{status}[/{color}] {claude_version}")
    except Exception:
        console.print(f"\nClaude CLI:")
        console.print(f"  [red]✗[/red] Not found or not accessible")

    # Check GitHub MCP
    try:
        result = subprocess.run(
            ["npx", "-y", "@modelcontextprotocol/server-github", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        status = "✓" if result.returncode == 0 else "✗"
        color = "green" if result.returncode == 0 else "red"
        console.print(f"\nGitHub MCP:")
        console.print(f"  [{color}]{status}[/{color}] Available via npx")
    except Exception:
        console.print(f"\nGitHub MCP:")
        console.print(f"  [red]✗[/red] Not accessible")

    console.print()


@cli.command()
def version():
    """Show version information"""
    from . import __version__
    console.print(f"\nVoice-Spec-Driven Development v{__version__}\n")


if __name__ == "__main__":
    cli()
