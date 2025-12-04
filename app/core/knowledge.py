import sqlite3
import sqlite_vec
import google.generativeai as genai
import struct
import os
from pathlib import Path
from typing import List

DB_PATH = Path.home() / ".local" / "share" / "sensei" / "knowledge.db"

def serialize_float32(vector: List[float]) -> bytes:
    """Serializes a list of floats into a bytes object for sqlite-vec."""
    return struct.pack(f"{len(vector)}f", *vector)

class LocalKnowledge:
    """RAG system using SQLite + sqlite-vec."""
    
    SEARCH_PATHS = [
        Path("/usr/share/doc/blackfin"),
        Path.home() / "Projects/blackfin/files/usr/share/doc/blackfin",
        Path("."), 
    ]

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
        self._init_db()
        if api_key:
            self._index_docs()

    def _init_db(self):
        if not DB_PATH.parent.exists():
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.enable_load_extension(True)
        sqlite_vec.load(self.conn)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                content TEXT,
                hash TEXT UNIQUE
            )
        """)
        
        self.conn.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS vec_items USING vec0(
                embedding FLOAT[768]
            )""")
        self.conn.commit()

    def _get_embedding(self, text: str, task_type="retrieval_document") -> List[float]:
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type=task_type
            )
            return result['embedding']
        except Exception as e:
            print(f"[Knowledge] Embedding error: {e}")
            return [0.0] * 768

    def _index_docs(self):
        for path in self.SEARCH_PATHS:
            if path.exists():
                for file in path.glob("*.md"):
                    self._process_file(file)

    def _process_file(self, file_path: Path):
        try:
            content = file_path.read_text(encoding="utf-8")
            import hashlib
            file_hash = hashlib.md5(content.encode()).hexdigest()
            
            cursor = self.conn.execute("SELECT 1 FROM documents WHERE filename = ? AND hash = ?", (file_path.name, file_hash))
            if cursor.fetchone():
                return

            print(f"[Knowledge] Indexing {file_path.name}...")
            embedding = self._get_embedding(content)
            
            cursor = self.conn.execute(
                "INSERT OR REPLACE INTO documents (filename, content, hash) VALUES (?, ?, ?)",
                (file_path.name, content, file_hash)
            )
            row_id = cursor.lastrowid
            
            self.conn.execute(
                "INSERT INTO vec_items(rowid, embedding) VALUES (?, ?)",
                (row_id, serialize_float32(embedding))
            )
            self.conn.commit()
            
        except Exception as e:
            print(f"[Knowledge] Failed to index {file_path.name}: {e}")

    def get_context(self) -> str:
        """Legacy compatibility method."""
        return "Local Documentation is indexed. Ask specific questions to retrieve context."

    def search(self, query: str, limit: int = 3) -> str:
        if not self.api_key:
            return ""
            
        query_embedding = self._get_embedding(query, task_type="retrieval_query")
        
        cursor = self.conn.execute("""
            SELECT 
                d.filename, 
                d.content,
                distance
            FROM vec_items v
            JOIN documents d ON v.rowid = d.rowid
            WHERE v.embedding MATCH ?
            AND k = ?
            ORDER BY distance
        """, (serialize_float32(query_embedding), limit))
        
        results = []
        for row in cursor.fetchall():
            filename, content, distance = row
            results.append(f"--- SOURCE: {filename} (Score: {distance:.4f}) ---\n{content}\n")
        
        if not results:
            return ""
            
        return "\n".join(results)
