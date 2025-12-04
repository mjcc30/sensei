# Changelog

All notable changes to this project will be documented in this file.

## [v2.2.0] - 2025-12-04

### New Features

- **Persistent Memory:** Sensei now remembers past conversations using SQLite (`~/.local/share/sensei/memory.db`).
- **Vector RAG:** Local documentation is indexed via `sqlite-vec` and Gemini Embeddings (`text-embedding-004`) for semantic search.

### Improvements

- Added End-to-End (E2E) Smoke Test (`tests/test_e2e.py`) to prevent broken releases.
- Refactored `Knowledge` module to support vector search while maintaining backward compatibility.

### Fixes

- Resolved syntax errors in RAG module (`unterminated f-string`).
- Fixed import issues in Dockerfile for robust server execution.

## [v2.1.0] - 2025-12-04

### New Features

- **Self-Update:** Added `sensei update` command to download the latest binary from GitHub Releases.

### Improvements

- **Router Optimization:** Implemented "Reframing Attack" logic in RouterAgent to rephrase user queries into formal academic requests, bypassing LLM safety filters for authorized research.

## [v2.0.4] - 2025-12-04

### New Features

- **MCP Server:** Created `app/server.py` using FastMCP to expose tools (Nmap) via Model Context Protocol.
- **FastAPI:** Added `app/api.py` to expose Sensei as a microservice (HTTP API).
- **Docker:** Added Dockerfile and workflow for building the MCP server image.

## [v1.0.0] - 2025-12-04

### Initial Release

- **Smart Fallback:** Interactive Chat and CLI Mode.
- **Swarm Architecture:** 3-Tier Agents (Novice/Researcher/Master).
- **Nuitka Build:** Single binary distribution.
