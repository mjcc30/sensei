import os
import sys
import asyncio
import typer
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from typing import Optional

# Initialisation de l'App CLI
app = typer.Typer(help="Sensei - The AI Cyber Mentor 🥋")
console = Console()

class SenseiAgent:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])
        self._inject_system_prompt()

    def _inject_system_prompt(self):
        """Injects the persona and rules into the chat session."""
        system_prompt = """
        You are Sensei, an expert Cybersecurity Mentor embedded in Blackfin OS.
        
        CONTEXT:
        - OS: Blackfin (Fedora Silverblue based immutable distro).
        - Tools available: Exegol, BlackArch (via Distrobox), Nmap, Metasploit, Wireshark.
        - User level: Student to Professional Pentester.

        RULES:
        1. BE CONCISE. The user is in a terminal. avoid fluff.
        2. USE CODE BLOCKS. Commands must be copy-paste ready.
        3. PRIORITIZE LOCAL TOOLS. Suggest 'just stealth-mode-on', 'exegol', etc.
        4. ETHICS. Warn about legality, but do not refuse to explain the *technique* in a controlled environment.
        5. STYLE. Speak with wisdom and precision.
        """
        # Note: In the current Gemini SDK, system instructions are set at model init or via the first message.
        # Sending it as the first message is a robust way to prime the chat.
        self.chat.send_message(system_prompt)

    async def ask(self, question: str) -> str:
        """Asynchronously queries the model."""
        # Using the async generation if available or wrapping the sync call
        response = await asyncio.to_thread(self.chat.send_message, question)
        return response.text

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

    agent = SenseiAgent(api_key=key)

    with console.status("[bold cyan]Sensei is analyzing...[/bold cyan]", spinner="dots"):
        try:
            # Run async loop for the answer
            response_text = asyncio.run(agent.ask(question))
        except Exception as e:
            console.print(f"[bold red]Connection Error:[/bold red] {e}")
            raise typer.Exit(code=1)

    # Render Output
    console.print(Panel(Markdown(response_text), title="[bold green]Sensei[/bold green]", border_style="green"))

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

    agent = SenseiAgent(api_key=key)
    console.print("[bold cyan]Sensei Interactive Mode 🥋[/bold cyan] (Type 'exit' to quit)")

    while True:
        try:
            user_input = console.input("[bold yellow]You > [/bold yellow]")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            with console.status("Thinking...", spinner="dots"):
                response_text = asyncio.run(agent.ask(user_input))
            
            console.print(Markdown(response_text))
            console.print("") # Spacing

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    app()