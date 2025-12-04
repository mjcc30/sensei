import os
import sys
import asyncio
import typer
import requests
import shutil
from pathlib import Path
from packaging import version
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table # Added for history command
from typing import Optional
from app.agents.orchestrator import Orchestrator
from app.core.memory import Memory # Added for history/clear commands

# Constantes
CURRENT_VERSION = "2.2.0" # À mettre à jour à chaque release
GITHUB_REPO = "mjcc30/sensei"

# Initialisation de l'App CLI
app = typer.Typer(help="Sensei - The AI Cyber Mentor 🥋")
console = Console()

# --- CLI Commands ---

@app.command()
def history(session_id: Optional[str] = None):
    """
    List past conversation sessions or display messages from a specific session.
    """
    memory = Memory()
    if session_id:
        console.print(f"[bold]History for session: {session_id}[/bold]")
        messages = memory.get_history(session_id=session_id)
        if not messages:
            console.print("No messages found for this session.")
            return
        for msg in messages:
            role_color = "blue" if msg["role"] == "user" else "green"
            console.print(f"[{role_color}]{msg["role"]}:[/] {msg["parts"][0]}")
    else:
        console.print("[bold]Recent Conversation Sessions:[/bold]")
        sessions = memory.list_sessions()
        if not sessions:
            console.print("No sessions found.")
            return
        
        table = Table(title="Sessions", show_lines=True)
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Last Active", style="yellow")
        for s_id, title, last_active in sessions:
            table.add_row(s_id, title, last_active)
        console.print(table)


@app.command()
def clear(all: bool = False, session_id: Optional[str] = None):
    """
    Clear conversation history (all sessions or a specific one).
    """
    memory = Memory()
    if all:
        confirm = typer.confirm("[red]Are you sure you want to delete ALL conversation history?[/red]")
        if confirm:
            memory.clear_all_history()
            console.print("[green]All conversation history cleared.[/green]")
        else:
            console.print("Operation cancelled.")
    elif session_id:
        confirm = typer.confirm(f"[red]Are you sure you want to delete session {session_id}?[/red]")
        if confirm:
            memory.clear_session(session_id)
            console.print(f"[green]Session {session_id} cleared.[/green]")
        else:
            console.print("Operation cancelled.")
    else:
        console.print("[yellow]Please specify --all or --session <ID> to clear history.[/yellow]")


@app.command()
def ask(
    question: str = typer.Argument(..., help="The question for Sensei"),
    key: Optional[str] = typer.Option(None, envvar="GEMINI_API_KEY", help="Google Gemini API Key"),
    verbose: bool = False
):
    """
    Ask a single question to Sensei.
    """
    if not key:
        console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not found.")
        console.print("Export it: [yellow]export GEMINI_API_KEY='...'[/yellow]")
        raise typer.Exit(code=1)

    # Initialize Swarm Orchestrator
    try:
        orch = Orchestrator(api_key=key)
    except Exception as e:
        console.print(f"[bold red]Init Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    with console.status("[bold cyan]Sensei Swarm is analyzing...[/bold cyan]", spinner="dots"):
        try:
            # Run async loop for the answer
            response_text = asyncio.run(orch.handle_request(question))
        except Exception as e:
            console.print(f"[bold red]Connection Error:[/bold red] {e}")
            raise typer.Exit(code=1)

    # Render Output (Clean up the [AgentID] prefix for cleaner display)
    if "]" in response_text:
        agent_id, content = response_text.split("]", 1)
        agent_id = agent_id.strip("[")
        title = f"[bold green]Sensei ({agent_id})[/bold green]"
    else:
        content = response_text
        title = "[bold green]Sensei[/bold green]"

    console.print(Panel(Markdown(content), title=title, border_style="green"))

@app.command()
def chat(
    key: Optional[str] = typer.Option(None, envvar="GEMINI_API_KEY"),
):
    """
    Start an interactive mentoring session.
    """
    if not key:
        console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not found.")
        raise typer.Exit(code=1)

    orch = Orchestrator(api_key=key)
    console.print("[bold cyan]Sensei Interactive Mode 🥋[/bold cyan] (Type 'exit' to quit)")
    console.print("[dim]Swarm Architecture Active[/dim]")

    while True:
        try:
            user_input = console.input("[bold yellow]You > [/bold yellow]")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            with console.status("Routing...", spinner="dots"):
                response_text = asyncio.run(orch.handle_request(user_input))
            
            # Clean display
            if "]" in response_text:
                agent_id, content = response_text.split("]", 1)
                console.print(f"[dim bold]{agent_id}[/dim bold]")
            else:
                content = response_text

            console.print(Markdown(content))
            console.print("") # Spacing

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    app()