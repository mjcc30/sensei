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

### 🔌 Phase 2: Tooling & MCP (Infrastructure First)

- [ ] **MCP Server:** Expose local tools (Nmap, Searchsploit) via Model Context Protocol.
- [ ] **ActionAgent:** Create an agent capable of executing safe commands via MCP.

### 🚧 Phase 3: Domain Specialization (Option B)

- [ ] **Domain Router:** Upgrade RouterAgent to classify by Domain (Red/Blue/OSINT/Cloud/Crypto).
- [ ] **Specialized Agents:**
  - `RedTeamMaster`: Focus on Exploitation & Evasion (Uses MCP Tools).
  - `BlueTeamResearcher`: Focus on Forensics, Logs Analysis & Defense.
  - `OsintAgent`: Focus on Recon & Intel.
  - `CloudAgent`: Focus on AWS/Azure/GCP misconfigurations.
  - `CryptoAgent`: Focus on Cryptography, Steganography & Mathematics.

### 🚀 Phase 4: Release

- [ ] **Merge:** Integrate `v2-swarm` into `main.py`.
- [ ] **Release:** v2.0.0.

### 🏛️ Phase 5: Architecture Evolution (v3.0 - The Rust Rewrite)

> Goal: Transform Sensei into a native, high-performance system tool using Rust.

- [ ] **Language Migration:** Rewrite core logic from Python to **Rust**.
  - Utilize `google-cloud-rs` (official SDK) for Gemini.
  - Utilize `modelcontextprotocol/rust-sdk` for MCP support.
- [ ] **Sensei Server (Rust):**
  - High-performance Async Server (Tokio/Axum).
  - Native implementation of A2A Bus without Python overhead.
- [ ] **Sensei Client (Rust):**
  - Instant startup CLI (Clap/Ratatui).
  - Single static binary distribution (5MB vs 30MB+).
- [ ] **Distributed Swarm:**
  - Allow agents to run on different machines (e.g., ReconAgent on a VPS, ReportAgent on local).

### 🧹 Technical Debt & Refactoring

- [ ] **Dynamic Versioning:** Stop hardcoding version strings in `main.py`. Read from `pyproject.toml` (Python) or `Cargo.toml` (Rust).

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
