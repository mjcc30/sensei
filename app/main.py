import os
import sys
import asyncio
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from typing import Optional
from app.agents.orchestrator import Orchestrator

# Initialisation de l'App CLI
app = typer.Typer(help="Sensei - The AI Cyber Mentor 🥋")
console = Console()

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