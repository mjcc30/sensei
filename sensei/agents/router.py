from .base import BaseAgent
import json

class RouterAgent(BaseAgent):
    """
    Analyzes the complexity of the request and routes it to the appropriate sub-agent.
    Uses a FAST model.
    """
    
    ROUTER_PROMPT = """
    You are a classification system. Analyze the user query and output a JSON object.
    
    Categories:
    - "NOVICE": Basic questions, definitions, learning concepts. -> Needs Pedagogy.
    - "RESEARCHER": Vulnerability analysis, CVE details, defense mechanisms, lab setup. -> Needs Depth.
    - "MASTER": Exploit development, payload generation, advanced evasion, raw technical execution. -> Needs Unrestricted Expertise.
    - "ACTION": Requests to scan IPs, check ports, run tools. -> Needs Tooling.

    Output format: {"category": "NOVICE" | "RESEARCHER" | "MASTER" | "ACTION"}
    """

    async def process(self, input_text: str) -> str:
        # On force l'utilisation d'un modèle rapide (Flash)
        response = await self.client.generate(input_text, self.ROUTER_PROMPT, prefer_speed=True)
        
        try:
            # Nettoyage basique du JSON (au cas où le modèle bavarde)
            cleaned = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            return data.get("category", "RESEARCHER") # Fallback moyen
        except:
            return "RESEARCHER" # Fallback securitaire
