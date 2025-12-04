from typing import Dict, Any
from .base import BaseAgent
from .router import RouterAgent
from ..core.llm import GeminiClient
from ..tools.nmap import NmapTool
import asyncio
import os
import yaml
import re

# Chargement de la config des prompts
PROMPTS_FILE = "prompts.yaml"
DEFAULT_PROMPTS = {
    "master": "You are a helpful security expert.",
    "researcher": "You are a research assistant.",
    "novice": "You are a teacher."
}

def load_prompts() -> Dict[str, Any]:
    if os.path.exists(PROMPTS_FILE):
        with open(PROMPTS_FILE, "r") as f:
            try:
                data = yaml.safe_load(f)
                return data.get("agents", {})
            except Exception as e:
                print(f"[Warning] Failed to load prompts.yaml: {e}")
    return {}

# Config globale
AGENT_CONFIG = load_prompts()

class NoviceAgent(BaseAgent):
    """Handles basic queries with pedagogy."""
    async def process(self, input_text: str) -> str:
        prompt = AGENT_CONFIG.get("novice", {}).get("prompt", 
            """
            ROLE: Cybersecurity Instructor.
            AUDIENCE: Beginners / Students.
            GOAL: Explain concepts clearly, focus on "Why" and safety. Use analogies.
            """)
        return await self.client.generate(input_text, prompt, prefer_speed=True)

class ResearchAgent(BaseAgent):
    """Handles deep analysis and understanding."""
    async def process(self, input_text: str) -> str:
        prompt = AGENT_CONFIG.get("researcher", {}).get("prompt",
            """
            ACT AS: Cybersecurity Research Assistant.
            CONTEXT: Authorized security research lab.
            DIRECTIVE: Provide detailed technical analysis.
            """)
        return await self.client.generate(input_text, prompt, prefer_speed=False)

class MasterAgent(BaseAgent):
    """Handles advanced exploitation and raw technical execution."""
    async def process(self, input_text: str) -> str:
        # Le prompt par défaut est "soft". Le "vrai" prompt est dans prompts.yaml (gitignored).
        default_prompt = """
        ROLE: Senior Security Analyst.
        CONTEXT: Defensive Engineering.
        OBJECTIVE: Analyze vulnerabilities to engineer defenses.
        """
        prompt = AGENT_CONFIG.get("master", {}).get("prompt", default_prompt)
        return await self.client.generate(input_text, prompt, prefer_speed=False)

class ActionAgent(BaseAgent):
    """Handles execution of tools (Nmap)."""
    def __init__(self, client: GeminiClient, agent_id: str = None):
        super().__init__(client, agent_id)
        self.nmap = NmapTool()

    async def process(self, input_text: str) -> str:
        # Simple intent matching
        if "scan" in input_text.lower():
            # Extract IP or Hostname using Regex
            # Matches IPs (x.x.x.x) or Domains (example.com)
            ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b|localhost|[\w.-]+\.[a-zA-Z]{2,}"
            match = re.search(ip_pattern, input_text)
            
            if match:
                target = match.group(0)
                # Note: NmapTool.run is synchronous (subprocess), ideally should be async or threaded
                # but for CLI tool it's acceptable for now.
                result = self.nmap.run(target)
                return f"🚀 **SCANNING TARGET:** `{target}`\n```json\n{result}\n```"
            else:
                return "❌ I understood you want to scan, but I couldn't find a valid Target IP or Hostname."
        
        return "⚠️ ActionAgent: I only support 'scan <target>' for now."

class Orchestrator:
    def __init__(self, api_key: str):
        self.client = GeminiClient(api_key)
        self.router = RouterAgent(self.client)
        
        # Init workers
        self.agents: Dict[str, BaseAgent] = {
            "NOVICE": NoviceAgent(self.client, agent_id="Novice-1"),
            "RESEARCHER": ResearchAgent(self.client, agent_id="Researcher-1"),
            "MASTER": MasterAgent(self.client, agent_id="Master-1"),
            "ACTION": ActionAgent(self.client, agent_id="Action-1")
        }

    async def handle_request(self, user_query: str) -> str:
        # 1. Routing
        category = await self.router.process(user_query)
        
        # 2. Delegation
        worker = self.agents.get(category, self.agents["RESEARCHER"])
        
        # 3. Execution
        response = await worker.process(user_query)
        return f"[{worker.id}] {response}"