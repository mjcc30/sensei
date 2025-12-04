import pytest
from pathlib import Path
from app.core.knowledge import LocalKnowledge

def test_load_knowledge(tmp_path):
    """Test that LocalKnowledge initializes correctly and indicates docs are indexed."""
    # Create dummy doc directory and file
    d = tmp_path / "doc"
    d.mkdir()
    p = d / "test_doc.md"
    p.write_text("# Test Documentation Content")
    
    # Monkeypatch SEARCH_PATHS (for test isolation)
    original_paths = LocalKnowledge.SEARCH_PATHS
    LocalKnowledge.SEARCH_PATHS = [d]
    
    try:
        kb = LocalKnowledge(api_key="dummy_key") # API key needed for indexing
        context = kb.get_context()
        
        assert "Local Documentation is indexed. Ask specific questions to retrieve context." in context
        # Verify that indexing was attempted
        assert kb.conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0] > 0
    finally:
        # Restore original paths
        LocalKnowledge.SEARCH_PATHS = original_paths

@pytest.mark.skip(reason="MCP server test needs a robust client or specific environment")
def test_mcp_server_tools_list():
    # This test is kept for reference but skipped due to current environment limitations
    pass

@pytest.mark.skip(reason="Docker MCP test needs docker and robust server")
def test_docker_mcp_handshake():
    # This test is kept for reference but skipped due to current environment limitations
    pass