import asyncio
import httpx
import time
import os
from typing import Any, Optional
from dataclasses import dataclass

@dataclass
class APIResponse:
    success: bool
    data: Any
    error: Optional[str]
    status_code: int
    response_time: float

class BulletproofClient:
    def __init__(self) -> None:
        base = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
        self.base_url = base
        self.timeout = httpx.Timeout(30.0, connect=10.0)
        self.max_retries = 3
        self.retry_delay = 1.0
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=100),
        )
        # Circuit breaker
        self._failure_count = 0
        self._failure_threshold = 5
        self._open_until = 0.0
        self._open_cooldown_s = 15.0

    async def call_ollama(self, model: str, prompt: str) -> APIResponse:
        start_time = time.time()

        now = time.time()
        if now < self._open_until:
            return APIResponse(
                success=False,
                data="",
                error="circuit_open",
                status_code=503,
                response_time=time.time() - start_time,
            )

        for attempt in range(self.max_retries):
            try:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "top_p": 0.9},
                }
                response = await self._client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                if response.status_code == 200:
                    self._failure_count = 0
                    result = response.json()
                    return APIResponse(
                        success=True,
                        data=result.get("response", ""),
                        error=None,
                        status_code=200,
                        response_time=time.time() - start_time,
                    )
                # non-200 -> treat as failure
            except (httpx.TimeoutException, httpx.ConnectError):
                # retryable
                pass
            except Exception:
                # retryable generic error
                pass

            # backoff
            if attempt < self.max_retries - 1:
                delay = self.retry_delay * (2 ** attempt)
                await asyncio.sleep(delay)

        # trip circuit
        self._failure_count += 1
        if self._failure_count >= self._failure_threshold:
            self._open_until = time.time() + self._open_cooldown_s

        return APIResponse(
            success=False,
            data="",
            error="Service unavailable",
            status_code=500,
            response_time=time.time() - start_time,
        )
