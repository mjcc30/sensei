from typing import Dict, Any, Optional
from .base import BaseAgent
from .router import RouterAgent
from ..core.llm import GeminiClient
from ..core.knowledge import LocalKnowledge
from ..core.memory import Memory
from ..tools.nmap import NmapTool
from ..tools.system import SystemTool
import asyncio
import os
import yaml
import re

# Chargement de la config des prompts
PROMPTS_FILE = "prompts.yaml"

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
            GOAL: Explain concepts clearly.
            """)
        return await self.client.generate(input_text, prompt, prefer_speed=True)

class SpecializedAgent(BaseAgent):
    """Generic class for domain experts (Red, Blue, Cloud, etc) using RAG."""
    def __init__(self, client, agent_id, role_key, knowledge=""):
        super().__init__(client, agent_id)
        self.role_key = role_key
        self.knowledge = knowledge

    async def process(self, input_text: str) -> str:
        # Load prompt dynamically based on role_key
        base_prompt = AGENT_CONFIG.get(self.role_key, {}).get("prompt", "You are a security expert.")
        
        # Inject RAG if available
        full_prompt = f"{base_prompt}\n{self.knowledge}"
        
        return await self.client.generate(input_text, full_prompt, prefer_speed=False)

class ActionAgent(BaseAgent):
    """Handles execution of tools (Nmap)."""
    def __init__(self, client: GeminiClient, agent_id: str = None):
        super().__init__(client, agent_id)
        self.nmap = NmapTool()

    async def process(self, input_text: str) -> str:
        if "scan" in input_text.lower():
            ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b|localhost|[\w.-]+\.[a-zA-Z]{2,}"
            match = re.search(ip_pattern, input_text)
            
            if match:
                target = match.group(0)
                result = self.nmap.run(target)
                return f"🚀 **SCANNING TARGET:** `{target}`\n```json\n{result}\n```"
            else:
                return "❌ I understood you want to scan, but I couldn't find a valid Target IP or Hostname."
        
        return "⚠️ ActionAgent: I only support 'scan <target>' for now."

class SystemAgent(BaseAgent):
    """Handles system diagnostics."""
    def __init__(self, client: GeminiClient, agent_id: str = None):
        super().__init__(client, agent_id)
        self.tool = SystemTool()

    async def process(self, input_text: str) -> str:
        # Auto-Diagnostic based on keywords
        context_data = []
        lower_input = input_text.lower()
        
        if any(k in lower_input for k in ["podman", "container", "docker"]):
            context_data.append(f"--- podman ps -a ---\n{self.tool.run('podman ps -a')}")
        
        if any(k in lower_input for k in ["ip", "network", "vpn", "interface", "wifi"]):
            context_data.append(f"--- ip a ---\n{self.tool.run('ip a')}")
            
        if any(k in lower_input for k in ["disk", "space", "storage", "df"]):
            context_data.append(f"--- df -h ---\n{self.tool.run('df -h')}")

        if any(k in lower_input for k in ["mem", "ram", "memory"]):
            context_data.append(f"--- free -m ---\n{self.tool.run('free -m')}")

        if any(k in lower_input for k in ["uptime", "load"]):
            context_data.append(f"--- uptime ---\n{self.tool.run('uptime')}")

        prompt = AGENT_CONFIG.get("system", {}).get("prompt", "Analyze the system state.")
        
        if context_data:
            full_input = f"USER QUERY: {input_text}\n\n>>> SYSTEM DIAGNOSTIC DATA:\n" + "\n".join(context_data)
        else:
            full_input = input_text
            
        return await self.client.generate(full_input, prompt, prefer_speed=False)

class CasualAgent(BaseAgent):
    """Handles general conversation."""
    async def process(self, input_text: str) -> str:
        prompt = AGENT_CONFIG.get("casual", {}).get("prompt", "You are a helpful CLI assistant.")
        return await self.client.generate(input_text, prompt, prefer_speed=True)

class Orchestrator:
    def __init__(self, api_key: str, session_id: str = None):
        self.client = GeminiClient(api_key)
        
        router_prompt = AGENT_CONFIG.get("router", {}).get("prompt")
        self.router = RouterAgent(self.client, prompt_template=router_prompt)
        
        self.knowledge = LocalKnowledge().get_context()
        self.memory = Memory()
        
        if session_id:
            self.memory.current_session_id = session_id
        elif not self.memory.current_session_id:
            last_id = self.memory.get_last_session()
            if last_id:
                self.memory.current_session_id = last_id
            else:
                self.memory.create_session()
        
        # Init workers
        self.agents: Dict[str, BaseAgent] = {
            "NOVICE": NoviceAgent(self.client, agent_id="Novice-1"),
            "ACTION": ActionAgent(self.client, agent_id="Action-1"),
            "SYSTEM": SystemAgent(self.client, agent_id="System-1"),
            "CASUAL": CasualAgent(self.client, agent_id="Casual-1"),
            
            # Domain Experts (Replaces generic Researcher/Master)
            "RED": SpecializedAgent(self.client, "RedTeam-1", "red_team", self.knowledge),
            "BLUE": SpecializedAgent(self.client, "BlueTeam-1", "blue_team", self.knowledge),
            "OSINT": SpecializedAgent(self.client, "Osint-1", "osint", self.knowledge),
            "CLOUD": SpecializedAgent(self.client, "Cloud-1", "cloud", self.knowledge),
            "CRYPTO": SpecializedAgent(self.client, "Crypto-1", "crypto", self.knowledge),
            
            # Fallbacks mapping (Legacy)
            "MASTER": SpecializedAgent(self.client, "RedTeam-1", "red_team", self.knowledge),
            "RESEARCHER": SpecializedAgent(self.client, "BlueTeam-1", "blue_team", self.knowledge),
        }

    async def handle_request(self, user_query: str) -> str:
        self.memory.add_message("user", user_query)
        
        routing_data = await self.router.process(user_query)
        category = routing_data["category"]
        optimized_query = routing_data.get("enhanced_query", user_query)
        
        # Default to CASUAL if unknown category
        worker = self.agents.get(category, self.agents["CASUAL"]) 
        
        response = await worker.process(optimized_query)
        self.memory.add_message("model", response)
        
        return f"[{worker.id}] {response}"