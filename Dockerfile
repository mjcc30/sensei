FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install system dependencies
# Nmap is required for the nmap_scan tool
RUN apt-get update && apt-get install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy configuration files
COPY pyproject.toml uv.lock ./
COPY README.md .

# Install python dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY app ./app

# Run the MCP Server
# Usage: docker run -i -e GEMINI_API_KEY=... ghcr.io/mjcc30/sensei-mcp
ENTRYPOINT ["uv", "run", "app/server.py"]
