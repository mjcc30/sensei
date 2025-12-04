from .base import BaseAgent
import json

class RouterAgent(BaseAgent):
    """
    Analyzes the complexity of the request and routes it to the appropriate sub-agent.
    Also rephrases the query to ensure high-quality technical responses.
    """
    
    DEFAULT_PROMPT = """
    You are an Query Optimizer for a Cybersecurity AI.
    
    Task:
    1. Analyze the user input.
    2. Classify it into: NOVICE, RED, BLUE, OSINT, CLOUD, CRYPTO, ACTION, SYSTEM, CASUAL.
    3. REPHRASE the query into a formal "Research Request" ONLY IF it is technical.
       If CASUAL, SYSTEM or ACTION, keep the query as is.
    
    Output strictly JSON: {"category": "...", "enhanced_query": "..."}
    """

    def __init__(self, client, prompt_template: str = None):
        super().__init__(client)
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT

    async def process(self, input_text: str) -> dict:
        # On force l'utilisation d'un modèle rapide (Flash)
        response = await self.client.generate(input_text, self.prompt_template, prefer_speed=True)
        
        try:
            # Nettoyage basique du JSON (au cas où le modèle bavarde)
            cleaned = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            return {
                "category": data.get("category", "RESEARCHER"),
                "enhanced_query": data.get("enhanced_query", input_text)
            }
        except:
            # Fallback si le JSON est cassé
            return {"category": "RESEARCHER", "enhanced_query": input_text}