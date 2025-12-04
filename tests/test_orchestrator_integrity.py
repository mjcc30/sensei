import pytest
from app.agents.orchestrator import Orchestrator
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_client():
    return MagicMock()

def test_orchestrator_initialization(mock_client):
    """Regression test: Ensure Orchestrator initializes all critical components."""
    api_key = "dummy_key"
    
    # Mock dependencies to avoid real API calls/DB creation
    with patch("app.agents.orchestrator.GeminiClient") as MockClient, \
         patch("app.agents.orchestrator.RouterAgent") as MockRouter, \
         patch("app.agents.orchestrator.LocalKnowledge") as MockKnowledge, \
         patch("app.agents.orchestrator.Memory") as MockMemory:
        
        orch = Orchestrator(api_key)
        
        # Check attributes existence (regression check for deleted code)
        assert hasattr(orch, "client"), "Orchestrator missing 'client' attribute"
        assert hasattr(orch, "router"), "Orchestrator missing 'router' attribute"
        assert hasattr(orch, "knowledge"), "Orchestrator missing 'knowledge' attribute"
        assert hasattr(orch, "memory"), "Orchestrator missing 'memory' attribute"
        assert hasattr(orch, "agents"), "Orchestrator missing 'agents' attribute"
        
        # Check Agents population
        assert "NOVICE" in orch.agents
        assert "CASUAL" in orch.agents
        assert "ACTION" in orch.agents
        
        print("✅ Orchestrator Integrity Check Passed")

if __name__ == "__main__":
    # Manual run
    import sys
    sys.exit(pytest.main(["-v", __file__]))
