# Zero-Cost AI Marketplace

A clean, modular MVP for an enterprise-ready AI marketplace with a minimal professional chat interface, FastAPI backend, mock AI models for development, and deployment tooling.

## Key Features
- Minimal, professional ChatGPT-style UI (dark theme)
- FastAPI backend with model routing, analytics, and customer tiers
- Mock AI models simulating GPT-OSS:20B and Llama with realistic latency
- Dockerized services and env configuration for fast deployment
- SQLite-ready (upgradeable), simple business analytics scaffolding

## Quick Start (Local)

1. Requirements
   - Python 3.10+
   - Node 18+ (optional, for frontend dev server)
   - Docker (optional, for containers)

2. Install Python deps
```bash
cd zero-cost-ai-marketplace
python -m venv .venv && . .venv/Scripts/activate  # Windows Powershell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Start backend
```bash
uvicorn backend.api.main:app --reload --port 8001
```

4. Open frontend
- Option A: Open `frontend/chat-interface/index.html` directly in your browser
- Option B: Run a simple server
```bash
# Node (recommended for CORS headers during dev)
npx http-server ./frontend -p 8080 -c-1 --cors
# or Python
python -m http.server 8080 -d frontend
```

5. Chat
- The chat UI posts to `http://localhost:8001/ai/generate`
- Backend returns mock responses with 2-5s latency

## Run with Docker
```bash
cd zero-cost-ai-marketplace
docker compose up --build
# Frontend: http://localhost:8080
# Backend:  http://localhost:8001/docs
```

## Project Structure
See the repository root for the full tree. Major areas:
- `frontend/` minimal chat UI and placeholders for admin dashboard
- `backend/` FastAPI app, routers, config, business logic
- `ai-integration/` smart router and mock models (swap for local models later)
- `deployment/` Dockerfiles, scripts, and docs
- `business/` marketplace logic, analytics, customer tiers
- `tests/` unit + integration scaffolding

## Environment
Create a `.env` at repo root (see `env.example`) and adjust as needed.

## Notes
- This MVP favors clarity and simplicity. Replace mock models in `ai-integration/local-models/` when ready.
- Analytics are in-memory to start. Swap to a database (SQLite/Postgres) as you scale.
