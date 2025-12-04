#!/bin/bash
# Point d'entrée pour l'extension Gemini CLI
cd "$(dirname "$0")"
export GEMINI_API_KEY="${GEMINI_API_KEY:-$1}" # Prend la clé de l'env ou du premier argument

if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY is required."
    exit 1
fi

# Lance le mode chat ou l'outil demandé
# Note: Pour une vraie intégration MCP, il faudrait un serveur stdio/http.
# Ici, on lance simplement l'outil.
uv run main.py chat --key "$GEMINI_API_KEY"
