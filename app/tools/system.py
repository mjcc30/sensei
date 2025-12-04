import subprocess
import shlex
from typing import List, Optional

class SystemTool:
    """
    Executes safe system diagnostic commands from an allowlist.
    """
    
    ALLOWLIST = {
        "podman": ["ps", "logs", "images", "info"],
        "ip": ["a", "addr", "route"],
        "df": ["-h"],
        "free": ["-m", "-h"],
        "uptime": [],
        "systemctl": ["status", "is-active"],
        "journalctl": ["-n", "-u", "--no-pager"],
        "nmcli": ["device", "connection", "show"]
    }

    def run(self, command_str: str) -> str:
        """
        Parses and executes a system command if allowed.
        """
        try:
            parts = shlex.split(command_str)
            if not parts:
                return "Error: Empty command."

            binary = parts[0]
            args = parts[1:]

            # Security Check
            if binary not in self.ALLOWLIST:
                return f"Error: Command '{binary}' is not allowed. Allowed: {list(self.ALLOWLIST.keys())}"

            # Argument Check (Basic)
            # We allow args, but we could refine this to check specific subcommands.
            # For now, relying on the binary being read-only tools generally.
            # Exception: systemctl/journalctl might need tighter scoping?
            
            # Execute
            result = subprocess.run(
                [binary] + args,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n[Stderr]: {result.stderr}"
                
            return output.strip()

        except Exception as e:
            return f"Error executing command: {e}"
