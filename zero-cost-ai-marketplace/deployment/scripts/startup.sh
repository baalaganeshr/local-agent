#!/bin/bash
set -e

echo "Starting bulletproof AI marketplace..."

if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "Attempting to start Ollama via Docker Compose (if configured)..."
  (cd "$(dirname "$0")/../docker" && docker compose -f docker-compose.ollama.yml up -d ollama) || true
  sleep 10
fi

# Ensure models present (best-effort)
command -v ollama >/dev/null 2>&1 && {
  ollama pull llama3.2:3b 2>/dev/null || true
  ollama pull gpt-oss:20b 2>/dev/null || true
}

while true; do
  uvicorn backend.api.main:app --host 0.0.0.0 --port 8001 || true
  echo "Application exited. Restarting in 5 seconds..."
  sleep 5
done
