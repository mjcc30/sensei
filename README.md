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
pip install -r requirements.txt
python sensei.py "How do I scan for SMB vulnerabilities?"
```

## 🤖 Usage
Set your API Key once:
```bash
export GEMINI_API_KEY="your_key_here"
```
Run interactive mode:
```bash
python sensei.py --chat
```
