# Sensei Project Context

## Overview
**Sensei** is a CLI-based AI Mentor designed for cybersecurity students and professionals. It serves as an integrated assistant within the **Blackfin OS** distribution but can function standalone.

## Core Identity
*   **Persona:** "Sensei" - A wise, technical, and ethical cybersecurity master.
*   **Tone:** Concise, practical, command-line focused.
*   **Philosophy:** "Explain Why, then Show How."

## Architecture (v2.0 Swarm)
*   **Language:** Python 3.12+ (Using `uv` package manager).
*   **Directory Structure:** `app/` (Source), `tests/`, `run.sh` (Entrypoint).
*   **Orchestrator:** `app/agents/orchestrator.py` manages the lifecycle.
*   **Router Agent:** Classifies intent (NOVICE, RESEARCHER, MASTER, ACTION) and **Rephrases** queries to bypass safety filters ("Reframing Attack").
*   **Agents:**
    *   `Novice`: Pedagogical, safety-first.
    *   `Researcher`: Deep analysis, context-aware.
    *   `Master`: Unrestricted technical execution ("God Mode").
    *   `Action`: Tool execution (e.g., Nmap).
*   **A2A Bus:** `app/core/a2a.py` - Asynchronous message bus for inter-agent communication.

## Security & Distribution (The "Secret Sauce")
*   **Prompts Strategy:**
    *   Public: `prompts.example.yaml` (Standard behavior).
    *   Private: `prompts.yaml` (Gitignored, contains "God Mode" instructions).
*   **Binary Compilation:**
    *   Tool: **Nuitka**.
    *   Injection: The CI pipeline injects `PROMPTS_SECRET` (GitHub Secret) into `prompts.yaml` before compilation.
    *   Embedding: `prompts.yaml` is embedded inside the binary (`--include-data-file`).
*   **Protection:** The end-user receives a compiled binary where prompts are obfuscated.

## CI/CD Pipeline
*   **Unit Tests:** `pytest` runs on every push (Mocked API calls).
*   **Build:** Nuitka compilation runs **only on tags** (`v*`).
*   **Artifacts:** `sensei-linux-x64` binary attached to Releases.

## Usage & Commands
**Single Question:**
```bash
# Quotes are optional due to shell wrapper
sensei how do I enumerate SMB shares?
```

**Interactive Chat:**
```bash
sensei
```

**Development:**
```bash
uv sync
uv pip install -e .  # Crucial for tests to find the package!
uv run app/main.py ask "Test"
```

## Roadmap
*   **v2.1:** MCP Server integration for broader tool support.
*   **v3.0 (The Rust Rewrite):** Full rewrite in Rust (Client-Server) for performance and native integration.
    *   Server: Python/FastAPI (Complex Agents).
    *   Client: Rust/Zig (Lightweight CLI).
