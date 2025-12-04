# Sensei Development Roadmap

## 📅 Status: Q4 2025 - v2.2.0 Released

Sensei is now a Multi-Agent Orchestrator with persistent memory and vector RAG.

---

## 🎯 v2.0 - The Swarm (Active Development)

### ✅ Phase 1: Core Architecture (Done)

- [x] **A2A Bus:** Implemented lightweight async message bus (`core/a2a.py`).
- [x] **Orchestrator:** 3-Tier Routing Logic (Novice / Researcher / Master).
- [x] **Adaptive Persona:** Dynamic system prompts based on user intent (Pedagogy vs Unrestricted).
- [x] **TDD:** Integration tests validation (`tests/test_swarm.py`).

### 🔌 Phase 2: Tooling & MCP (Infrastructure First)

- [x] **MCP Server:** Expose local tools (Nmap) via Model Context Protocol (`app/server.py`).
- [ ] **ActionAgent Client:** Refactor ActionAgent to communicate with the MCP Server via JSON-RPC (Currently uses direct Python import).

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

## 🛠️ v2.2.0 - Enhancements

- [x] **Persistent Memory:** Sensei now remembers past conversations using SQLite.
- [x] **Vector RAG:** Local documentation is indexed via `sqlite-vec` and Gemini Embeddings.
- [ ] **Local LLM Support:** Add support for Ollama/Llama.cpp via `langchain` or direct API.
- [ ] **Blackfin Integration:** Add a specific tool to control `ghost-shell` directly from Sensei.
