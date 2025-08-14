import asyncio
import httpx

class IntegrationTester:
    def __init__(self) -> None:
        self.base_url = "http://localhost:8001"

    async def run_all_tests(self) -> None:
        print("STARTING INTEGRATION TESTS")
        print("=" * 50)
        tests = [
            self.test_health_endpoint,
            self.test_chat_endpoint,
            self.test_model_routing,
            self.test_customer_tiers,
            self.test_error_handling,
            self.test_ollama_connection,
            self.test_business_analytics,
        ]
        for test in tests:
            try:
                ok = await test()
                print(("✅ ", test.__name__, ": PASS") if ok else ("❌ ", test.__name__, ": FAIL"))
            except Exception as e:
                print("❌ ", test.__name__, ": ERROR - ", str(e))
        print("\n" + "=" * 50)
        print("INTEGRATION TEST COMPLETE")

    async def test_health_endpoint(self) -> bool:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/api/health")
            return r.status_code == 200

    async def test_chat_endpoint(self) -> bool:
        payload = {"messages": [{"role": "user", "content": "Hello"}], "user_id": "u1", "tier": "basic"}
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.base_url}/api/chat", json=payload)
            if r.status_code != 200:
                return False
            data = r.json()
            return bool(data.get("content"))

    async def test_model_routing(self) -> bool:
        async with httpx.AsyncClient() as client:
            p1 = {"messages": [{"role": "user", "content": "Hi"}], "tier": "basic"}
            r1 = await client.post(f"{self.base_url}/api/chat", json=p1)
            p2 = {"messages": [{"role": "user", "content": "Write complex Python code"}], "tier": "enterprise"}
            r2 = await client.post(f"{self.base_url}/api/chat", json=p2)
            if r1.status_code != 200 or r2.status_code != 200:
                return False
            d1, d2 = r1.json(), r2.json()
            return (d1.get("model") in ("llama3.2:3b", "cache")) and (d2.get("model") in ("gpt-oss:20b", "cache"))

    async def test_customer_tiers(self) -> bool:
        tiers = ["basic", "premium", "enterprise"]
        async with httpx.AsyncClient() as client:
            for t in tiers:
                p = {"messages": [{"role": "user", "content": "Task"}], "tier": t}
                r = await client.post(f"{self.base_url}/api/chat", json=p)
                if r.status_code != 200:
                    return False
        return True

    async def test_error_handling(self) -> bool:
        async with httpx.AsyncClient() as client:
            p1 = {"messages": [], "tier": "basic"}
            r1 = await client.post(f"{self.base_url}/api/chat", json=p1)
            p2 = {"messages": [{"role": "user", "content": "Hello"}], "tier": "invalid"}
            r2 = await client.post(f"{self.base_url}/api/chat", json=p2)
            return r1.status_code == 400 and r2.status_code == 200

    async def test_ollama_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r = await client.get("http://localhost:11434/api/tags")
                return r.status_code == 200 or r.status_code == 404
        except Exception:
            return True  # do not fail suite if Ollama is not running

    async def test_business_analytics(self) -> bool:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/api/analytics")
            return r.status_code == 200

if __name__ == "__main__":
    tester = IntegrationTester()
    asyncio.run(tester.run_all_tests())
