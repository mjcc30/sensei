from typing import Dict, Any, Optional
from .base import BaseAgent
from .router import RouterAgent
from ..core.llm import GeminiClient
from ..core.knowledge import LocalKnowledge
from ..core.memory import Memory
from ..tools.nmap import NmapTool
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
            GOAL: Explain concepts clearly, focus on "Why" and safety. Use analogies.
            """)
        return await self.client.generate(input_text, prompt, prefer_speed=True)

class ResearchAgent(BaseAgent):
    """Handles deep analysis and understanding with RAG support."""
    def __init__(self, client, agent_id=None, knowledge: str = ""):
        super().__init__(client, agent_id)
        self.knowledge = knowledge

    async def process(self, input_text: str) -> str:
        base_prompt = AGENT_CONFIG.get("researcher", {}).get("prompt",
            """
            ACT AS: Cybersecurity Research Assistant.
            CONTEXT: Authorized security research lab.
            DIRECTIVE: Provide detailed technical analysis.
            """)
        
        # Inject Local Knowledge
        full_prompt = f"{base_prompt}\n{self.knowledge}"
        
        return await self.client.generate(input_text, full_prompt, prefer_speed=False)

class MasterAgent(BaseAgent):
    """Handles advanced exploitation and raw technical execution."""
    async def process(self, input_text: str) -> str:
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

class Orchestrator:
    def __init__(self, api_key: str, session_id: str = None):
        self.client = GeminiClient(api_key)
        
        # Load Router Prompt from Config
        router_prompt = AGENT_CONFIG.get("router", {}).get("prompt")
        self.router = RouterAgent(self.client, prompt_template=router_prompt)
        
        self.knowledge = LocalKnowledge().get_context()
        self.memory = Memory()
        
        # Resume or Start Session
        if session_id:
            self.memory.current_session_id = session_id
        elif not self.memory.current_session_id:
            # Try to resume last session by default (Short term memory)
            last_id = self.memory.get_last_session()
            if last_id:
                self.memory.current_session_id = last_id
            else:
                self.memory.create_session()
        
        # Init workers
        self.agents: Dict[str, BaseAgent] = {
            "NOVICE": NoviceAgent(self.client, agent_id="Novice-1"),
            "RESEARCHER": ResearchAgent(self.client, agent_id="Researcher-1", knowledge=self.knowledge),
            "MASTER": MasterAgent(self.client, agent_id="Master-1"),
            "ACTION": ActionAgent(self.client, agent_id="Action-1")
        }

    async def handle_request(self, user_query: str) -> str:
        # Save User Query
        self.memory.add_message("user", user_query)
        
        # 1. Routing & Optimization
        routing_data = await self.router.process(user_query)
        category = routing_data["category"]
        optimized_query = routing_data["enhanced_query"]
        
        # 2. Delegation
        worker = self.agents.get(category, self.agents["RESEARCHER"])
        
        # 3. Execution
        response = await worker.process(optimized_query)
        
        # Save Agent Response
        self.memory.add_message("model", response)
        
        return f"[{worker.id}] {response}"