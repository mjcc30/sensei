import google.generativeai as genai
from google.api_core import exceptions
import asyncio

class GeminiClient:
    """Wrapper for Google Gemini API with smart fallback."""
    
    MODELS_PREFERENCE = [
        "gemini-3-pro-preview",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]

    FAST_MODELS = [
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = None
        self.model_name = ""

    def get_model(self, prefer_speed: bool = False):
        """Returns an initialized generative model."""
        models_to_try = self.FAST_MODELS if prefer_speed else self.MODELS_PREFERENCE
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                self.model_name = model_name
                return model
            except Exception:
                continue
        
        # Fallback global si le mode "speed" échoue
        if prefer_speed:
             return self.get_model(prefer_speed=False)
             
        raise Exception("No Gemini models available.")

    async def generate(self, prompt: str, system_instruction: str = "", prefer_speed: bool = False) -> str:
        model = self.get_model(prefer_speed)
        
        # Note: System instructions are better handled via a chat session or prepended
        full_prompt = f"{system_instruction}\n\nUser Query: {prompt}"
        
        response = await asyncio.to_thread(model.generate_content, full_prompt)
        return response.text
