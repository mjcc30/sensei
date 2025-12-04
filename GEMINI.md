# Sensei Project Context

## Overview
**Sensei** is a CLI-based AI Mentor designed for cybersecurity students and professionals. It serves as an integrated assistant within the **Blackfin OS** distribution but can function standalone.

## Core Identity
*   **Persona:** "Sensei" - A wise, technical, and ethical cybersecurity master.
*   **Tone:** Concise, practical, command-line focused.
*   **Philosophy:** "Explain Why, then Show How."

## Architecture
*   **Language:** Python 3.12+
*   **Package Manager:** `uv` (Modern Python packager).
*   **Dependencies:**
    *   `google-generativeai`: For LLM capabilities (Gemini 1.5 Flash).
    *   `typer`: For CLI argument parsing.
    *   `rich`: For beautiful terminal output (Markdown rendering).
    *   `asyncio`: For non-blocking API calls.

## Usage
**Single Question:**
```bash
uv run main.py ask "How do I enumerate SMB shares?"
```

**Interactive Chat:**
```bash
uv run main.py chat
```

## Configuration
Requires environment variable: `GEMINI_API_KEY`.

## Development Goals
*   Future integration with MCP (Model Context Protocol).
*   Local LLM support (Ollama).
*   Deep integration with Blackfin OS tools (Justfile, Ghost Shell).

## 🔬 R&D / Future Vision (v2.0 - The Swarm)
> Implementation of Multi-Agent Systems (MAS) inspired by [Gemini Flow](https://github.com/clduab11/gemini-flow).

*   **Architecture:** Transition from Single Agent to Orchestrator.
*   **Protocols:** Implement A2A (Agent-to-Agent) and MCP for seamless context sharing.
*   **Specialization:** Sub-agents for Recon, Exploit, and Reporting.

