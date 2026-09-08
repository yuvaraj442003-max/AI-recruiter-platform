"""
test_redis_and_dual_db.py — Comprehensive tests for Redis Caching Layer & Dual Database Support.
Tests:
1. Redis cache operations (set, get, set_json, get_json, delete, delete_pattern)
2. Redis status reporting
3. Database status & dialect reporting (PostgreSQL and SQLite)
4. GET /api/v1/system/status health endpoint
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import get_db_status
from app.services.redis_service import (
    cache_delete,
    cache_delete_pattern,
    cache_get,
    cache_get_json,
    cache_set,
    cache_set_json,
    get_redis_status,
)

client = TestClient(app)


def test_redis_cache_set_and_get():
    key = "test_key_123"
    val = "Hello Redis Cache"

    # Set cache
    success = cache_set(key, val, ttl_seconds=60)
    assert success is True

    # Get cache
    retrieved = cache_get(key)
    assert retrieved == val

    # Delete cache
    cache_delete(key)
    assert cache_get(key) is None


def test_redis_cache_json():
    key = "test_json_key_456"
    data = {
        "job_id": "999-aaa-bbb",
        "ats_match_score": 92.5,
        "matched_skills": ["Python", "FastAPI", "PostgreSQL", "Redis"],
    }

    # Set JSON cache
    success = cache_set_json(key, data, ttl_seconds=120)
    assert success is True

    # Get JSON cache
    retrieved = cache_get_json(key)
    assert retrieved == data

    # Clean up
    cache_delete(key)
    assert cache_get_json(key) is None


def test_redis_cache_delete_pattern():
    cache_set("ats_rank:job_1", "data_1")
    cache_set("ats_rank:job_2", "data_2")
    cache_set("ats_rank:job_3", "data_3")

    count = cache_delete_pattern("ats_rank:*")
    assert count >= 3
    assert cache_get("ats_rank:job_1") is None


def test_redis_status():
    status = get_redis_status()
    assert "enabled" in status
    assert "connected" in status
    assert "backend_type" in status
    assert status["connected"] is True


def test_database_status():
    db_info = get_db_status()
    assert "dialect" in db_info
    assert "connected" in db_info
    assert db_info["connected"] is True
    assert db_info["dialect"] in ["postgresql", "sqlite"]


def test_system_status_endpoint():
    resp = client.get("/api/v1/system/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True

    sys_data = data["data"]
    assert "databases" in sys_data
    assert "redis_cache" in sys_data
    assert sys_data["databases"]["connected"] is True
    assert sys_data["redis_cache"]["connected"] is True
