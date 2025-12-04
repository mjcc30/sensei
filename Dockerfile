FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install system dependencies
# Nmap is required for the nmap_scan tool
RUN apt-get update && apt-get install -y \
    nmap \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy configuration files
COPY pyproject.toml uv.lock ./
COPY README.md .

# Install python dependencies
RUN uv sync --frozen --no-dev

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy source code
COPY app ./app

# Run the MCP Server directly with python (avoids uv startup logs on stdout)
# Usage: docker run -i -e GEMINI_API_KEY=... ghcr.io/mjcc30/sensei-mcp
ENTRYPOINT ["python", "app/server.py"]
