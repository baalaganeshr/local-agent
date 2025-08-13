import asyncio
import httpx
import time
import statistics
import psutil

class PerformanceTest:
    def __init__(self) -> None:
        self.base_url = "http://localhost:8001"

    async def test_response_times(self) -> bool:
        times = []
        async with httpx.AsyncClient() as client:
            for _ in range(5):
                start = time.time()
                r = await client.post(f"{self.base_url}/api/chat", json={"messages":[{"role":"user","content":"Hello"}]})
                end = time.time()
                if r.status_code == 200:
                    times.append(end - start)
        if not times:
            return False
        avg = statistics.mean(times)
        print(f"Average response time: {avg:.2f}s")
        return avg < 3.0

    async def test_concurrent_users(self) -> bool:
        async def single():
            async with httpx.AsyncClient() as client:
                r = await client.post(f"{self.base_url}/api/chat", json={"messages":[{"role":"user","content":"Test concurrent"}]})
                return r.status_code == 200
        results = await asyncio.gather(*[single() for _ in range(10)])
        success_rate = sum(1 for x in results if x) / len(results)
        print(f"Concurrent user success rate: {success_rate:.0%}")
        return success_rate >= 0.9

    def test_system_resources(self) -> bool:
        mem = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=1)
        print(f"Memory usage: {mem:.1f}% | CPU: {cpu:.1f}%")
        return mem < 80 and cpu < 80

if __name__ == "__main__":
    perf = PerformanceTest()
    ok1 = asyncio.run(perf.test_response_times())
    ok2 = asyncio.run(perf.test_concurrent_users())
    ok3 = perf.test_system_resources()
    print("PASS" if all([ok1, ok2, ok3]) else "FAIL")
