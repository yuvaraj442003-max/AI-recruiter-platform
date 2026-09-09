"""
redis_service.py — Production-grade Redis Caching Layer for AI Recruiter Platform.
Provides high-performance caching for ATS matches, job recommendations, session invalidation,
and LLM response caching. Uses real Redis if available, or fakeredis fallback.
"""
import json
import logging
import socket
from typing import Any, Optional

import fakeredis
import redis

from app.core.config import settings

logger = logging.getLogger("ai_recruiter.redis")

_redis_client: Optional[redis.Redis] = None
_backend_type: str = "none"


def _is_redis_port_open(host: str, port: int, timeout: float = 0.2) -> bool:
    """Fast socket check to verify if Redis port is open before attempting client connection."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def _try_autostart_redis(host: str, port: int) -> bool:
    """Attempts to auto-launch redis-server background process if running locally and port is closed."""
    if host not in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
        return False
    try:
        import subprocess
        import time

        kwargs = {}
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        logger.info("Attempting to auto-start local redis-server process...")
        subprocess.Popen(["redis-server"], **kwargs)
        time.sleep(1.2)
        return _is_redis_port_open(host, port, timeout=0.5)
    except Exception as e:
        logger.debug(f"Auto-start redis-server attempt failed: {e}")
        return False


def init_redis_client() -> redis.Redis:
    """Initializes the Redis client (Real Redis or FakeRedis in-memory fallback)."""
    global _redis_client, _backend_type

    if _redis_client is not None:
        return _redis_client

    if not settings.REDIS_ENABLED:
        logger.info("Redis is disabled in settings. Initializing in-memory FakeRedis.")
        _redis_client = fakeredis.FakeRedis(decode_responses=True)
        _backend_type = "fakeredis_disabled"
        return _redis_client

    host = settings.REDIS_HOST or "localhost"
    port = settings.REDIS_PORT or 6379

    # Fast pre-check: test socket connection to Redis port, try auto-starting if closed
    if not _is_redis_port_open(host, port, timeout=0.1):
        _try_autostart_redis(host, port)

    if _is_redis_port_open(host, port, timeout=0.2):
        try:
            if settings.REDIS_URL:
                client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_timeout=1.0)
            else:
                client = redis.Redis(
                    host=host,
                    port=port,
                    password=settings.REDIS_PASSWORD or None,
                    db=settings.REDIS_DB,
                    decode_responses=True,
                    socket_timeout=1.0,
                )
            try:
                client.ping()
            except redis.exceptions.ResponseError as r_err:
                if "MISCONF" in str(r_err):
                    client.config_set("stop-writes-on-bgsave-error", "no")
                    client.ping()
                else:
                    raise r_err
            _redis_client = client
            _backend_type = "redis_live"
            logger.info(f"Connected to live Redis server at {host}:{port}")
            print(f"[REDIS CONNECTED] High-performance caching layer active via Redis ({host}:{port})")
            return _redis_client
        except Exception as err:
            logger.warning(f"Could not connect to live Redis ({err}). Falling back to in-memory FakeRedis.")

    # Fallback to FakeRedis in-memory caching layer
    logger.info("Live Redis server not reached. Using in-memory FakeRedis caching layer.")
    print("[REDIS FALLBACK] Live Redis not reached. Using in-memory FakeRedis layer.")
    _redis_client = fakeredis.FakeRedis(decode_responses=True)
    _backend_type = "fakeredis_fallback"
    return _redis_client


def get_redis_client() -> redis.Redis:
    """Returns the singleton Redis client instance."""
    if _redis_client is None:
        return init_redis_client()
    return _redis_client


def cache_get(key: str) -> Optional[str]:
    """Retrieves a string value from Redis cache by key."""
    try:
        client = get_redis_client()
        val = client.get(key)
        if val is not None:
            logger.debug(f"Redis Cache HIT: {key}")
        else:
            logger.debug(f"Redis Cache MISS: {key}")
        return val
    except Exception as err:
        logger.error(f"Redis cache_get error for key '{key}': {err}")
        return None


def cache_set(key: str, value: str, ttl_seconds: Optional[int] = None) -> bool:
    """Stores a string value in Redis cache with an optional TTL (expiration in seconds)."""
    try:
        client = get_redis_client()
        ttl = ttl_seconds if ttl_seconds is not None else settings.CACHE_DEFAULT_TTL_SECONDS
        client.set(name=key, value=value, ex=ttl)
        logger.debug(f"Redis Cache SET: {key} (TTL={ttl}s)")
        return True
    except Exception as err:
        logger.error(f"Redis cache_set error for key '{key}': {err}")
        return False


def cache_get_json(key: str) -> Optional[Any]:
    """Retrieves and deserializes a JSON object from Redis cache."""
    val = cache_get(key)
    if val is None:
        return None
    try:
        return json.loads(val)
    except Exception as err:
        logger.error(f"Failed to parse JSON cache for key '{key}': {err}")
        return None


def cache_set_json(key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
    """Serializes a Python object to JSON and stores it in Redis cache."""
    try:
        json_str = json.dumps(value, default=str)
        return cache_set(key, json_str, ttl_seconds)
    except Exception as err:
        logger.error(f"Failed to serialize JSON for key '{key}': {err}")
        return False


def cache_delete(key: str) -> bool:
    """Deletes a key from Redis cache."""
    try:
        client = get_redis_client()
        client.delete(key)
        return True
    except Exception as err:
        logger.error(f"Redis cache_delete error for key '{key}': {err}")
        return False


def cache_delete_pattern(pattern: str) -> int:
    """Deletes all Redis keys matching a glob pattern (e.g. 'ats_ranking:*')."""
    try:
        client = get_redis_client()
        keys = client.keys(pattern)
        if keys:
            count = client.delete(*keys)
            logger.info(f"Cleared {count} cached keys matching pattern '{pattern}'")
            return count
        return 0
    except Exception as err:
        logger.error(f"Redis cache_delete_pattern error for pattern '{pattern}': {err}")
        return 0


def get_redis_status() -> dict:
    """Returns Redis connection status and performance metadata."""
    try:
        client = get_redis_client()
        ping_ok = client.ping()
        keys_count = len(client.keys("*"))
        return {
            "enabled": settings.REDIS_ENABLED,
            "connected": bool(ping_ok),
            "backend_type": _backend_type,
            "keys_cached": keys_count,
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
        }
    except Exception as err:
        return {
            "enabled": settings.REDIS_ENABLED,
            "connected": False,
            "backend_type": _backend_type,
            "error": str(err),
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
        }
