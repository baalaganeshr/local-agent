# Zero-Cost AI Marketplace

A clean, modular MVP for an enterprise-ready AI marketplace with integrated chat interface, FastAPI backend, local AI models, and full static file serving.

## Key Features
- **Integrated Chat Interface**: Professional ChatGPT-style UI served directly from the backend
- **FastAPI Backend**: Complete API with model routing, analytics, and customer tiers  
- **Static File Serving**: Frontend assets served by FastAPI with CORS configured
- **Local AI Models**: Zero-cost operation with gpt-oss:20b and llama3.2:3b
- **One-Command Startup**: Single script launches complete integrated system
- **Production Ready**: Docker support and deployment tooling included

## 🚀 Quick Start

### Integrated System (Recommended)
Start the complete integrated system with chat interface:

```bash
cd zero-cost-ai-marketplace
pip install -r requirements.txt
python start_backend.py
```

Then open your browser to:
- **Chat Interface**: http://localhost:8001/
- **API Health**: http://localhost:8001/api/health  
- **API Docs**: http://localhost:8001/docs

### Manual Backend Only
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
