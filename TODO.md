# Sensei Development Roadmap

## 📅 Status: Q4 2025 - v1.0 Released

Sensei is currently a Single-Agent CLI tool. The goal is to evolve it into a Multi-Agent Orchestrator.

---

## 🎯 v2.0 - The Swarm (R&D)
> Inspired by [Gemini Flow](https://github.com/clduab11/gemini-flow).

- [ ] **Architecture Transition:**
    - Refactor `main.py` to support multiple agent classes.
    - Implement a Supervisor Agent (Orchestrator).

- [ ] **Specialized Agents:**
    - `ReconAgent`: Specialized in Nmap, Masscan, Whois.
    - `ExploitAgent`: Specialized in Searchsploit, Metasploit, CVEs.
    - `ReportAgent`: Specialized in summarizing findings into Markdown/SysReptor format.

- [ ] **Protocols:**
    - **MCP (Model Context Protocol):** Implement a standardized way for agents to share scan results (JSON/XML).
    - **A2A (Agent-to-Agent):** Enable agents to query each other (e.g., ExploitAgent asks ReconAgent for open ports).

---

## 🛠️ v1.x - Enhancements
- [ ] **Local LLM Support:** Add support for Ollama/Llama.cpp via `langchain` or direct API.
- [ ] **Conversation History:** Persist chat history between sessions (local SQLite or JSON).
- [ ] **RAG (Retrieval Augmented Generation):** Allow Sensei to index local documentation (`/usr/share/doc/blackfin`) for better answers.
- [ ] **Blackfin Integration:** Add a specific tool to control `ghost-shell` directly from Sensei.

---

## 📝 Changelog
### v1.0.0
- Initial Release.
- Features: Smart Fallback, Interactive Chat, CLI Mode.
