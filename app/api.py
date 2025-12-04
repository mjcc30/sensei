from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app.agents.orchestrator import Orchestrator
import os

app = FastAPI(title="Sensei API", version="2.1.0")

class QueryRequest(BaseModel):
    query: str
    api_key: str = None

class QueryResponse(BaseModel):
    response: str
    agent: str

@app.post("/ask", response_model=QueryResponse)
async def ask_sensei(request: QueryRequest):
    # Use provided key or env var
    key = request.api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise HTTPException(status_code=401, detail="API Key required")

    try:
        orch = Orchestrator(api_key=key)
        full_response = await orch.handle_request(request.query)
        
        # Parse "[Agent] Content"
        if "]" in full_response:
            agent_id, content = full_response.split("]", 1)
            agent_id = agent_id.strip("[")
        else:
            agent_id = "Unknown"
            content = full_response

        return {"response": content.strip(), "agent": agent_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.1.0"}
