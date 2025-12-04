from mcp.server.fastmcp import FastMCP
from app.tools.nmap import NmapTool

# Création du serveur "Sensei Tools"
mcp = FastMCP("Sensei Tools")

nmap_tool = NmapTool()

@mcp.tool()
def nmap_scan(target: str, quick: bool = True) -> str:
    """
    Scans a target IP for open ports using Nmap.
    
    Args:
        target: IP address or hostname to scan (e.g., '127.0.0.1', 'scanme.nmap.org').
        quick: If True, runs a fast scan (Top 100 ports). If False, runs a full service scan (-sV).
    """
    return nmap_tool.run(target, quick)

if __name__ == "__main__":
    # Par défaut, FastMCP écoute sur stdio
    mcp.run()
