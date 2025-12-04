import os
import sys
import asyncio
import typer
import google.generativeai as genai
from google.api_core import exceptions
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from typing import Optional

# Initialisation de l'App CLI
app = typer.Typer(help="Sensei - The AI Cyber Mentor 🥋")
console = Console()

# Modèles par ordre de préférence (Intelligence > Vitesse)
MODELS_TO_TRY = [
    "gemini-3-pro-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

class SenseiAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = None
        self.chat = None
        self.model_name = ""

    def initialize_model(self):
        """Tries to initialize the best available model from the list."""
        for model_name in MODELS_TO_TRY:
            try:
                # On tente de créer le modèle et de lancer une session
                model = genai.GenerativeModel(model_name)
                # Test de connexion silencieux (ping)
                # Note: start_chat ne fait pas d'appel réseau immédiat, mais on va assumer que ça passe
                # On configure l'agent avec ce modèle
                self.model = model
                self.model_name = model_name
                self.chat = self.model.start_chat(history=[])
                self._inject_system_prompt()
                return # Succès
            except Exception:
                continue # On essaie le suivant
        
        # Si aucun modèle ne marche
        raise Exception("No Gemini models available. Check your API Key and Region.")

    def _inject_system_prompt(self):
        """Injects the persona and rules into the chat session."""
        system_prompt = f"""
        You are Sensei, an expert Cybersecurity Mentor embedded in Blackfin OS.
        Running on Model: {self.model_name}
        
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
        self.chat.send_message(system_prompt)

    async def ask(self, question: str) -> str:
        """Asynchronously queries the model with fallback logic."""
        if not self.model:
            self.initialize_model()
        
        try:
            response = await asyncio.to_thread(self.chat.send_message, question)
            return response.text
        except exceptions.NotFound:
             # Si le modèle choisi crashe en cours de route (ex: déprécié), on pourrait retenter
             # Pour l'instant on remonte l'erreur
             return "Error: Model not found or API issue."

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
    console.print(Panel(Markdown(response_text), title=f"[bold green]Sensei ({agent.model_name})[/bold green]", border_style="green"))

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

    # Init model first to show which one is used
    try:
        agent.initialize_model()
        console.print(f"[dim]Connected to: {agent.model_name}[/dim]")
    except Exception as e:
        console.print(f"[bold red]Failed to init:[/bold red] {e}")
        return

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
