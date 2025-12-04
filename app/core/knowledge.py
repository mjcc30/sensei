import os
from pathlib import Path
from typing import List

class LocalKnowledge:
    """Simple RAG system for local documentation."""
    
    # Paths to search for documentation
    SEARCH_PATHS = [
        Path("/usr/share/doc/blackfin"),
        Path.home() / "Projects/blackfin/files/usr/share/doc/blackfin",
        Path("."), # Current dir (README.md)
    ]

    def __init__(self):
        self.context = ""
        self._load_knowledge()

    def _load_knowledge(self):
        """Loads all markdown files into memory context."""
        content = []
        
        for path in self.SEARCH_PATHS:
            if path.exists():
                for file in path.glob("*.md"):
                    try:
                        text = file.read_text(encoding="utf-8")
                        content.append(f"--- DOCUMENT: {file.name} ---\n{text}\n")
                    except Exception:
                        pass
        
        if content:
            self.context = "\n".join(content)
            print(f"[Knowledge] Loaded {len(content)} documents.")
        else:
            self.context = ""

    def get_context(self) -> str:
        """Returns the full documentation context for the LLM."""
        if not self.context:
            return ""
        
        return f"""
        
        === LOCAL DOCUMENTATION (CONTEXT) ===
        Use this information to answer questions about the local system/OS.
        {self.context}
        =====================================
        """
