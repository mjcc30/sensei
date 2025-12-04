import sqlite3
import json
import uuid
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

DB_PATH = Path.home() / ".local" / "share" / "sensei" / "memory.db"

@dataclass
class Message:
    role: str
    content: str
    timestamp: str

class Memory:
    def __init__(self):
        self._init_db()
        self.current_session_id = None

    def _init_db(self):
        """Initialize SQLite database and tables."""
        if not DB_PATH.parent.exists():
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create Tables
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES sessions(id)
            )
        """)
        self.conn.commit()

    def create_session(self, title: str = "New Chat") -> str:
        """Starts a new conversation session."""
        session_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO sessions (id, title) VALUES (?, ?)",
            (session_id, title)
        )
        self.conn.commit()
        self.current_session_id = session_id
        return session_id

    def get_last_session(self) -> Optional[str]:
        """Retrieves the most recent session ID."""
        self.cursor.execute("SELECT id FROM sessions ORDER BY last_active DESC LIMIT 1")
        row = self.cursor.fetchone()
        return row[0] if row else None

    def add_message(self, role: str, content: str, session_id: str = None):
        """Saves a message to the database."""
        sid = session_id or self.current_session_id
        if not sid:
            sid = self.create_session()
        
        self.cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (sid, role, content)
        )
        # Update session timestamp
        self.cursor.execute(
            "UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE id = ?",
            (sid,)
        )
        self.conn.commit()

    def get_history(self, session_id: str = None, limit: int = 50) -> List[Dict[str, str]]:
        """Loads message history for context injection."""
        sid = session_id or self.current_session_id
        if not sid:
            return []
            
        self.cursor.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC LIMIT ?",
            (sid, limit)
        )
        rows = self.cursor.fetchall()
        # Format for Gemini: [{"role": "user", "parts": [...]}, ...]
        return [{"role": row[0], "parts": [row[1]]} for row in rows]

    def list_sessions(self):
        """Returns recent conversations."""
        self.cursor.execute("SELECT id, title, last_active FROM sessions ORDER BY last_active DESC LIMIT 10")
        return self.cursor.fetchall()
