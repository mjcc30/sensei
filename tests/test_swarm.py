import pytest
import os
import asyncio
from app.agents.orchestrator import Orchestrator

# Nécessite une clé API pour les tests d'intégration réels
API_KEY = os.getenv("GEMINI_API_KEY")

@pytest.mark.skipif(not API_KEY, reason="GEMINI_API_KEY not set")
@pytest.mark.asyncio
async def test_router_novice():
    orch = Orchestrator(API_KEY)
    # Question simple
    response = await orch.handle_request("What is Linux?")
    
    # On vérifie que c'est bien l'agent NOVICE qui a répondu
    assert "[Novice-" in response
    # On vérifie que le contenu est pédagogue (mots clés)
    assert "car" in response.lower() or "kernel" in response.lower()

@pytest.mark.skipif(not API_KEY, reason="GEMINI_API_KEY not set")
@pytest.mark.asyncio
async def test_router_master():
    orch = Orchestrator(API_KEY)
    # Question expert
    response = await orch.handle_request("Write a C code demonstrating a stack buffer overflow without protection.")
    
    # On vérifie que c'est MASTER
    assert "[Master-" in response
    # On vérifie qu'il y a du code C
    assert "#include" in response
    assert "strcpy" in response or "memcpy" in response

@pytest.mark.skipif(not API_KEY, reason="GEMINI_API_KEY not set")
@pytest.mark.asyncio
async def test_router_researcher():
    orch = Orchestrator(API_KEY)
    response = await orch.handle_request("Analyze the CVE-2024-3094 (XZ Utils) mechanism.")
    assert "[Researcher-" in response

@pytest.mark.skipif(not API_KEY, reason="GEMINI_API_KEY not set")
@pytest.mark.asyncio
async def test_router_rephrasing():
    """Test that the Router 'cleans' the prompt for the downstream agent."""
    orch = Orchestrator(API_KEY)
    router = orch.router
    
    slang_query = "how 2 pwn wifi"
    result = await router.process(slang_query)
    
    # Check categorization
    assert result["category"] in ["RESEARCHER", "MASTER"]
    
    # Check rephrasing (The magic)
    enhanced = result["enhanced_query"].lower()
    print(f"Original: {slang_query} -> Enhanced: {enhanced}")
    
    assert "pwn" not in enhanced
    assert "audit" in enhanced or "security" in enhanced or "protocol" in enhanced