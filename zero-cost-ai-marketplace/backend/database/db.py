from __future__ import annotations
import os
import sqlite3
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
import uuid

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "app.db"))

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        tier TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        tier TEXT NOT NULL,
        prompt TEXT NOT NULL,
        response TEXT NOT NULL,
        model TEXT NOT NULL,
        latency_ms INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        user_id TEXT,
        rating INTEGER,
        comment TEXT,
        created_at TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        tier TEXT NOT NULL,
        amount REAL NOT NULL,
        cost REAL NOT NULL,
        margin REAL NOT NULL,
        created_at TEXT NOT NULL
    );
    """,
]


def _connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    con = _connect()
    try:
        cur = con.cursor()
        for stmt in _SCHEMA:
            cur.executescript(stmt)
        con.commit()
    finally:
        con.close()
    ensure_migrations()


def ensure_migrations() -> None:
    con = _connect()
    try:
        cur = con.cursor()
        # users: add email, api_key, last_active
        try:
            cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE users ADD COLUMN api_key TEXT")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE users ADD COLUMN last_active TEXT")
        except Exception:
            pass
        con.commit()
    finally:
        con.close()


def upsert_user(user_id: Optional[str], tier: str) -> None:
    if not user_id:
        return
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        now = datetime.utcnow().isoformat()
        if row:
            cur.execute("UPDATE users SET tier = ?, last_active = ? WHERE id = ?", (tier, now, user_id))
        else:
            cur.execute(
                "INSERT INTO users(id, name, tier, created_at, last_active) VALUES(?,?,?,?,?)",
                (user_id, None, tier, now, now),
            )
        con.commit()
    finally:
        con.close()


def create_user(email: str, tier: str = "basic") -> Tuple[str, str]:
    user_id = str(uuid.uuid4())
    api_key = uuid.uuid4().hex
    now = datetime.utcnow().isoformat()
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users(id, name, tier, created_at, last_active, email, api_key) VALUES(?,?,?,?,?,?,?)",
            (user_id, None, tier, now, now, email, api_key),
        )
        con.commit()
    finally:
        con.close()
    return user_id, api_key


def get_user_by_api_key(api_key: str) -> Optional[sqlite3.Row]:
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE api_key = ?", (api_key,))
        return cur.fetchone()
    finally:
        con.close()


def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cur.fetchone()
    finally:
        con.close()


def set_user_tier(user_id: str, tier: str) -> None:
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute("UPDATE users SET tier = ? WHERE id = ?", (tier, user_id))
        con.commit()
    finally:
        con.close()


def touch_user(user_id: Optional[str]) -> None:
    if not user_id:
        return
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute("UPDATE users SET last_active = ? WHERE id = ?", (datetime.utcnow().isoformat(), user_id))
        con.commit()
    finally:
        con.close()


def record_conversation(user_id: Optional[str], tier: str, prompt: str, response: str, model: str, latency_ms: int) -> int:
    con = _connect()
    try:
        cur = con.cursor()
        now = datetime.utcnow().isoformat()
        cur.execute(
            """
            INSERT INTO conversations(user_id, tier, prompt, response, model, latency_ms, created_at)
            VALUES(?,?,?,?,?,?,?)
            """,
            (user_id, tier, prompt, response, model, latency_ms, now),
        )
        conv_id = cur.lastrowid
        con.commit()
        return int(conv_id)
    finally:
        con.close()


_PRICING = {
    "basic": 0.01,
    "premium": 0.02,
    "enterprise": 0.05,
}


def record_billing(user_id: Optional[str], tier: str) -> Tuple[float, float, float]:
    amount = _PRICING.get(tier.lower(), 0.01)
    cost = round(amount * 0.05, 4)  # 95% margin target
    margin = round(amount - cost, 4)
    con = _connect()
    try:
        cur = con.cursor()
        now = datetime.utcnow().isoformat()
        cur.execute(
            "INSERT INTO billing(user_id, tier, amount, cost, margin, created_at) VALUES(?,?,?,?,?,?)",
            (user_id, tier, amount, cost, margin, now),
        )
        con.commit()
    finally:
        con.close()
    return amount, cost, margin


def insert_feedback(conversation_id: Optional[int], rating: Optional[int], comment: Optional[str], user_id: Optional[str]) -> None:
    con = _connect()
    try:
        cur = con.cursor()
        now = datetime.utcnow().isoformat()
        cur.execute(
            "INSERT INTO feedback(conversation_id, user_id, rating, comment, created_at) VALUES(?,?,?,?,?)",
            (conversation_id, user_id, rating, comment, now),
        )
        con.commit()
    finally:
        con.close()


def get_analytics() -> Dict[str, Any]:
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(1) AS c FROM conversations")
        total_conversations = int(cur.fetchone()["c"])

        cur.execute("SELECT SUM(amount) AS s FROM billing")
        total_revenue = float(cur.fetchone()["s"] or 0.0)

        cur.execute("SELECT SUM(cost) AS s FROM billing")
        total_cost = float(cur.fetchone()["s"] or 0.0)

        cur.execute("SELECT AVG(latency_ms) AS a FROM conversations")
        avg_latency_ms = int(cur.fetchone()["a"] or 0)

        cur.execute("SELECT tier, COUNT(1) AS c FROM conversations GROUP BY tier")
        tier_distribution = {row["tier"]: int(row["c"]) for row in cur.fetchall()}

        margin_pct = 0.0
        if total_revenue > 0:
            margin_pct = round(((total_revenue - total_cost) / total_revenue) * 100.0, 2)

        return {
            "total_conversations": total_conversations,
            "total_revenue": round(total_revenue, 4),
            "total_cost": round(total_cost, 4),
            "margin_percent": margin_pct,
            "avg_latency_ms": avg_latency_ms,
            "tier_distribution": tier_distribution,
        }
    finally:
        con.close()
