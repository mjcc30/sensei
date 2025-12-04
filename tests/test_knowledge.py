import pytest
from pathlib import Path
from app.core.knowledge import LocalKnowledge

def test_load_knowledge(tmp_path):
    """Test that LocalKnowledge correctly loads markdown files from a given directory."""
    # Create dummy doc directory and file
    d = tmp_path / "doc"
    d.mkdir()
    p = d / "test_doc.md"
    p.write_text("# Test Documentation Content")
    
    # Monkeypatch the SEARCH_PATHS to point to our temp dir
    # Note: Modifying the class attribute affects all instances, so we should be careful or restore it.
    # Better to use an instance or constructor arg, but for this test we'll patch.
    original_paths = LocalKnowledge.SEARCH_PATHS
    LocalKnowledge.SEARCH_PATHS = [d]
    
    try:
        kb = LocalKnowledge()
        context = kb.get_context()
        
        assert "Test Documentation Content" in context
        assert "test_doc.md" in context
        assert "=== LOCAL DOCUMENTATION (CONTEXT) ===" in context
    finally:
        # Restore
        LocalKnowledge.SEARCH_PATHS = original_paths

def test_empty_knowledge():
    """Test behavior when no docs are found."""
    original_paths = LocalKnowledge.SEARCH_PATHS
    LocalKnowledge.SEARCH_PATHS = [Path("/non/existent/path")]
    
    try:
        kb = LocalKnowledge()
        context = kb.get_context()
        assert context == ""
    finally:
        LocalKnowledge.SEARCH_PATHS = original_paths
