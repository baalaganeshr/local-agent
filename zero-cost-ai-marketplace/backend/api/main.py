from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Literal
import time
import logging

from backend.config.settings import settings
from backend.services.ai_service import generate_reply
from backend.services.ai_router import OllamaRouter
from backend.services.multi_agent_system import MultiAgentRouter
from backend.database.db import (
    init_db,
    upsert_user,
    record_conversation,
    record_billing,
    insert_feedback,
    get_analytics,
    get_user_by_api_key,
    create_user,
    touch_user,
)
from backend.utils.response_cleaner import ResponseCleaner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="Zero-Cost AI Marketplace API", version="0.5.1")
app.add_middleware(GZipMiddleware, minimum_size=512)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_REQUEST_LOG: dict[str, list[float]] = {}
_RATE_LIMIT_PER_HOUR = 100

router = OllamaRouter()
agents_router = MultiAgentRouter()
cleaner = ResponseCleaner()

class ChatMessage(BaseModel):
    role: Literal["user","assistant","system"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    user_id: Optional[str] = None
    tier: Optional[str] = None

class ChatResponse(BaseModel):
    content: str
    model: str
    latency_ms: int
    tier: str
    conversation_id: int

class FeedbackRequest(BaseModel):
    conversation_id: Optional[int] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    user_id: Optional[str] = None

@app.on_event("startup")
async def on_startup() -> None:
    init_db()

async def api_key_auth(request: Request) -> str:
    api_key = request.headers.get("x-api-key") or request.query_params.get("api_key")
    if not api_key:
        return "demo-user"
    row = get_user_by_api_key(api_key)
    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key")
    touch_user(row["id"])
    return row["id"]

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)
    logger.info("%s %s %s %dms", request.method, request.url.path, request.headers.get("x-api-key", "anon"), duration_ms)
    return response

@app.get("/api/health")
async def health():
    return {"status": "operational", "models_available": ["gpt-oss:20b", "llama3.2:3b"], "profit_margin": "95-98%"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, user_id: str = Depends(api_key_auth)):
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    now = time.time(); window_start = now - 3600
    hist = _REQUEST_LOG.setdefault(user_id, [])
    hist[:] = [t for t in hist if t >= window_start]
    if len(hist) >= _RATE_LIMIT_PER_HOUR:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    hist.append(now)

    last_user = next((m for m in reversed(req.messages) if m.role == "user"), None)
    if not last_user:
        raise HTTPException(status_code=400, detail="No user message found")

    tier = (req.tier or settings.default_tier).lower()
    upsert_user(user_id, tier)

    try:
        result = await router.generate_response(last_user.content, tier)
        content = result.get("response", "")
        model = result.get("model_used", "router")
        latency_ms = int((result.get("response_time", 0) or 0) * 1000)
    except Exception:
        content, model, latency_ms = await generate_reply(last_user.content, tier)

    content = cleaner.clean_response(content)
    conv_id = record_conversation(user_id, tier, last_user.content, content, model, latency_ms)
    record_billing(user_id, tier)

    return ChatResponse(content=content, model=model, latency_ms=latency_ms, tier=tier, conversation_id=conv_id)

# Multi-agent variant endpoint returning agent + model metadata
class AgentsChatRequest(BaseModel):
    message: str
    customer_tier: Optional[str] = "basic"

class AgentsChatResponse(BaseModel):
    success: bool
    response: str
    agent_used: str
    model_used: str
    response_time: float
    status: str

@app.post("/api/chat/agents", response_model=AgentsChatResponse)
async def chat_agents(req: AgentsChatRequest, user_id: str = Depends(api_key_auth)):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message required")
    tier = (req.customer_tier or settings.default_tier).lower()
    upsert_user(user_id, tier)
    result = await agents_router.process_request(req.message.strip(), tier)
    result["response"] = cleaner.clean_response(result.get("response", ""))
    return AgentsChatResponse(**result)

@app.get("/api/analytics")
async def analytics():
    return get_analytics()

@app.post("/api/feedback")
async def feedback(req: FeedbackRequest, user_id: str = Depends(api_key_auth)):
    insert_feedback(req.conversation_id, req.rating, req.comment, user_id)
    return {"status": "received"}

class RegisterRequest(BaseModel):
    email: str
    tier: Optional[str] = "basic"

class RegisterResponse(BaseModel):
    user_id: str
    api_key: str

@app.post("/api/auth/register", response_model=RegisterResponse)
async def register(req: RegisterRequest):
    if not req.email:
        raise HTTPException(status_code=400, detail="email required")
    user_id, api_key = create_user(req.email, req.tier or "basic")
    return RegisterResponse(user_id=user_id, api_key=api_key)
