# Sensei 🥋

### The AI Cyber Mentor for Hackers

**Sensei** is a CLI tool powered by Google Gemini, designed to assist penetration testers, CTF players, and cybersecurity students directly from their terminal.

## 🌟 Features

- **Context Aware:** Understands standard tools (Nmap, Metasploit, Burp).
- **Stealth & Ethics:** Warns about OpSec failures.
- **Terminal Beauty:** Rich markdown rendering.
- **Project Agnostic:** Works on any Linux distro (Kali, Blackfin, Ubuntu).

## 🚀 Installation

```bash
git clone https://github.com/mjcc30/sensei.git
cd sensei
uv sync
uv run main.py ask how do I scan for SMB vulnerabilities?
```

## 🤖 Usage

Set your API Key once:

```bash
export GEMINI_API_KEY="your_key_here"
```

**Quick Question:**

```bash
# No quotes needed!
uv run main.py ask how do I use nmap stealthily?
```

**Interactive Mode:**

```bash
uv run app/main.py chat
```

## 🔌 MCP Integration (Model Context Protocol)

Sensei exposes its tools (like Nmap) via a standard MCP Server. This allows other AI assistants (Claude Desktop, Gemini Advanced) to use Sensei's capabilities.

**Run the Server:**

```bash
uv run app/server.py
```

_(This starts a stdio JSON-RPC server)_

**Claude Desktop Configuration:**
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uv",
      "args": ["run", "/path/to/sensei/app/server.py"]
    }
  }
}
```

## ⚙️ Configuration & Customization

Sensei uses a default persona ("Helpful Mentor"). You can customize or override these prompts (e.g., for specialized research or Red Teaming) by creating a `prompts.yaml` file.

1.  Copy the example:
    ```bash
    cp prompts.example.yaml prompts.yaml
    ```
2.  Edit `prompts.yaml` to define your own System Prompts for each agent (Novice, Researcher, Master).
3.  **Note:** `prompts.yaml` is ignored by Git to protect your custom methodology or sensitive instructions.

## 🔬 Architecture (v2 - The Swarm)

Sensei uses a **Multi-Agent Orchestrator**:

1.  **Router:** Analyzes your query (Simple vs Complex).
2.  **Specialists:** Delegates to the best agent (Novice, Researcher, or Master).
3.  **A2A Bus:** Asynchronous internal communication.
