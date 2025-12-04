# Sensei Development Roadmap

## 📅 Status: Q4 2025 - v1.0 Released

Sensei is currently a Single-Agent CLI tool. The goal is to evolve it into a Multi-Agent Orchestrator.

---

## 🎯 v2.0 - The Swarm (Active Development)
> Branch: `v2-swarm`

### ✅ Phase 1: Core Architecture (Done)
- [x] **A2A Bus:** Implemented lightweight async message bus (`core/a2a.py`).
- [x] **Orchestrator:** 3-Tier Routing Logic (Novice / Researcher / Master).
- [x] **Adaptive Persona:** Dynamic system prompts based on user intent (Pedagogy vs Unrestricted).
- [x] **TDD:** Integration tests validation (`tests/test_swarm.py`).

### 🚧 Phase 2: Domain Specialization (Option B)
- [ ] **Domain Router:** Upgrade RouterAgent to classify by Domain (Red/Blue/OSINT/Cloud/Crypto).
- [ ] **Specialized Agents:**
    - `RedTeamMaster`: Focus on Exploitation & Evasion.
    - `BlueTeamResearcher`: Focus on Forensics, Logs Analysis & Defense.
    - `OsintAgent`: Focus on Recon & Intel.
    - `CloudAgent`: Focus on AWS/Azure/GCP misconfigurations.
    - `CryptoAgent`: Focus on Cryptography, Steganography & Mathematics.

### 🔌 Phase 3: Tooling & MCP
- [ ] **MCP Server:** Expose local tools (Nmap, Searchsploit) via Model Context Protocol.
- [ ] **ActionAgent:** Create an agent capable of executing safe commands via MCP.

### 🚀 Phase 4: Release

- [ ] **Merge:** Integrate `v2-swarm` into `main.py`.

- [ ] **Release:** v2.0.0.



### 🏛️ Phase 5: Architecture Evolution (v3.0)

> Transition from Monolithic CLI to Client-Server Architecture.



- [ ] **Sensei Server:**

    - Build a **FastAPI** backend to host agents and tools.

    - Implement MCP over SSE (Server-Sent Events) for remote control.

    - Generate OpenAPI/Swagger documentation for easy AI integration.

- [ ] **Sensei Client:**

    - Rewrite CLI as a lightweight client querying the local/remote server.

- [ ] **Distributed Swarm:**

    - Allow agents to run on different machines (e.g., ReconAgent on a VPS, ReportAgent on local).



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
