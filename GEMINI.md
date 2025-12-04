# Sensei Project Context

## Overview
**Sensei** is a CLI-based AI Mentor designed for cybersecurity students and professionals. It serves as an integrated assistant within the **Blackfin OS** distribution but can function standalone.

## Core Identity
*   **Persona:** "Sensei" - A wise, technical, and ethical cybersecurity master.
*   **Tone:** Concise, practical, command-line focused.
*   **Philosophy:** "Explain Why, then Show How."

## Architecture (v2.2 Swarm)
*   **Language:** Python 3.12+ (Using `uv` package manager).
*   **Directory Structure:** `app/` (Source), `tests/`, `run.sh` (Entrypoint).
*   **Orchestrator:** `app/agents/orchestrator.py` manages the lifecycle.
    *   *Critical:* Initializes Memory, Router, Knowledge, and Workers.
*   **Router Agent:** Classifies intent (NOVICE, RESEARCHER, MASTER, ACTION, CASUAL) and **Rephrases** technical queries.
    *   *Prompt:* Externalized in `prompts.yaml`.
*   **Agents:**
    *   `Novice`: Pedagogical.
    *   `Researcher`: Deep analysis with RAG.
    *   `Master`: Unrestricted technical execution ("God Mode").
    *   `Action`: Tool execution (e.g., Nmap).
    *   `Casual`: General conversation (New in v2.3).
*   **Memory:** SQLite-based persistent conversation history (`~/.local/share/sensei/memory.db`).
*   **Knowledge (RAG):** Vector search using `sqlite-vec` and Gemini Embeddings.

## Security & Distribution
*   **Prompts Strategy:** `prompts.example.yaml` (Public) vs `prompts.yaml` (Secret/Ignored).
*   **Binary Compilation:** Nuitka (Embeds prompts, creates standalone binary).
*   **Update:** Self-update mechanism via GitHub Releases.

## Development Protocols & Safety
*   **Tool Usage:**
    *   NEVER use `replace` with partial code blocks (e.g., `# ... existing code`). Always provide the full replacement content or use `write_file` to rewrite the entire file to avoid accidental code deletion.
    *   Always verify `old_string` matches exactly.
*   **Testing:**
    *   Run `test_e2e.py` (Smoke Test) after ANY modification to `main.py` or `orchestrator.py`.
    *   Run unit tests before pushing.

## Roadmap
*   **v3.0 (The Rust Rewrite):** Full rewrite in Rust (Client-Server) for performance.