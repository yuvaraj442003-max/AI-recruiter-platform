"""
check_redis.py — Diagnostics & Live Server Verification Utility.
Run this anytime to test the connection to your live Redis server:
    python scripts/check_redis.py
"""
import os
import sys
import time

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.services.redis_service import (
    get_redis_client,
    get_redis_status,
    init_redis_client,
    reset_redis_client,
)


def main():
    print("=" * 65)
    print("     AI RECRUITER — REDIS LIVE SERVER CONNECTION CHECK")
    print("=" * 65)

    print("\n[1] Environment Configuration:")
    print(f"    - REDIS_ENABLED  : {settings.REDIS_ENABLED}")
    print(f"    - REDIS_URL      : {settings.REDIS_URL or '(not set, using host/port)'}")
    print(f"    - REDIS_HOST     : {settings.REDIS_HOST}")
    print(f"    - REDIS_PORT     : {settings.REDIS_PORT}")
    print(f"    - REDIS_PASSWORD : {'******' if settings.REDIS_PASSWORD else '(none)'}")
    print(f"    - REDIS_DB       : {settings.REDIS_DB}")

    print("\n[2] Connecting to Redis...")
    reset_redis_client()
    start_t = time.perf_counter()
    client = init_redis_client()
    elapsed_ms = (time.perf_counter() - start_t) * 1000

    status = get_redis_status()

    print("\n[3] Connection Results:")
    print(f"    - Backend Type   : {status.get('backend_type')}")
    print(f"    - Live Connected : {status.get('is_live')}")
    print(f"    - Target Host    : {status.get('host')}:{status.get('port')}")
    print(f"    - TLS / SSL      : {status.get('is_tls')}")
    print(f"    - Latency (Init) : {elapsed_ms:.2f} ms")

    if status.get("is_live"):
        print("\n[+] SUCCESS: Connected to LIVE Redis Server! \u2705")
        try:
            info = client.info("server")
            print(f"    - Redis Version  : {info.get('redis_version', 'Unknown')}")
            print(f"    - OS             : {info.get('os', 'Unknown')}")
            print(f"    - Uptime (days)  : {info.get('uptime_in_days', 0)}")
        except Exception:
            pass

        # Perform Read/Write Test
        test_key = "test:ai_recruiter:ping"
        test_val = f"live_ok_{int(time.time())}"
        client.set(test_key, test_val, ex=10)
        retrieved = client.get(test_key)
        client.delete(test_key)

        if retrieved == test_val:
            print("    - Read/Write Test: PASSED \u2705 (Key set, read back, and cleaned up)")
        else:
            print("    - Read/Write Test: FAILED \u274c")

        print(f"    - Total Keys in DB: {status.get('keys_cached', 0)}")
        print("\nYour AI Recruiter caching layer is fully accelerated by Live Redis.")
        return 0

    else:
        print("\n[-] NOTICE: Running on In-Memory FakeRedis Fallback \u26a0\ufe0f")
        if status.get("error"):
            print(f"    Reason: {status.get('error')}")
        print("\nHow to connect to a Live Redis Server:")
        print("  1. LOCAL REDIS (Windows):")
        print("     - Ensure redis-server is started: run '.\\run_backend.ps1' or run 'redis-server' in terminal.")
        print("     - In backend/.env: REDIS_HOST=localhost, REDIS_PORT=6379, REDIS_ENABLED=True")
        print("  2. CLOUD REDIS (Upstash / Redis Cloud / AWS):")
        print("     - In backend/.env, set REDIS_URL to your live instance URL:")
        print("       REDIS_URL=rediss://default:YOUR_PASSWORD@YOUR_ENDPOINT.upstash.io:6379")
        return 1


if __name__ == "__main__":
    sys.exit(main())
