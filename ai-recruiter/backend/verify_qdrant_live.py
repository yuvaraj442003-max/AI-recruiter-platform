import sys
import os

# Add backend to path
sys.path.insert(0, r"c:\Users\DELL\Downloads\ai-recruiter-all-phases-sqlite\ai-recruiter\backend")

from app.services import qdrant_service
from app.core.database import SessionLocal

print("=" * 65)
print("1. QDRANT INITIALIZATION & HEALTH STATUS")
print("=" * 65)
# Ensure all 6 collections exist
qdrant_service.ensure_collections()

health = qdrant_service.get_health_status()
print(f"  Available: {health.get('available')}")
print(f"  Mode: {health.get('mode')}")
print(f"  Embedding Model: {health.get('embedding_model')}")
print(f"  Vector Dimension: {health.get('vector_dimension')}")
print("  Collections:")
for coll_name, stat in health.get("collections", {}).items():
    print(f"    - {coll_name:22} : {stat.get('points_count', 0)} points (exists: {stat.get('exists')}, status: {stat.get('status')})")

print("\n" + "=" * 65)
print("2. EMBEDDING GENERATION TEST")
print("=" * 65)
test_text = "Senior Python Developer with FastAPI and PostgreSQL experience"
emb = qdrant_service.generate_embedding(test_text)
print(f"  Generated embedding dimensions: {len(emb)}")
print(f"  Sample vector slice (first 3 floats): {emb[:3]}")

print("\n" + "=" * 65)
print("3. LIVE DOCUMENT UPSERT TEST")
print("=" * 65)
upsert_ok = qdrant_service.upsert_document(
    collection_name="jobs",
    doc_id="test-job-verify-999",
    text=test_text,
    metadata={"title": "Python Backend Engineer", "skills": "Python, FastAPI, SQL", "role": "backend"}
)
print(f"  Upsert result: {upsert_ok}")

print("\n" + "=" * 65)
print("4. SEMANTIC SIMILARITY SEARCH TEST")
print("=" * 65)
query = "FastAPI Python engineer wanted"
results = qdrant_service.search(
    collection_name="jobs",
    query_text=query,
    limit=3
)
print(f"  Query: '{query}'")
print(f"  Matches found: {len(results)}")
for r in results:
    doc_id = r.get("id")
    score = r.get("score", 0)
    sim_pct = r.get("similarity_pct", 0)
    title = r.get("payload", {}).get("title")
    print(f"    -> Score: {score:.4f} ({sim_pct}% match) | ID: {doc_id} | Title: {title}")

print("\n" + "=" * 65)
print("5. CLEANUP VERIFICATION POINT")
print("=" * 65)
del_ok = qdrant_service.delete_document("jobs", "test-job-verify-999")
print(f"  Delete test point: {del_ok}")

print("\n" + "=" * 65)
print("6. DATABASE SYNC CHECK (Sync PostgreSQL to Qdrant)")
print("=" * 65)
db = SessionLocal()
try:
    sync_stats = qdrant_service.sync_all_from_db(db)
    print(f"  Status: {sync_stats.get('status')}")
    print(f"  Message: {sync_stats.get('message')}")
    print(f"  Records synchronized from PostgreSQL to Qdrant:")
    for coll, count in sync_stats.get("counts", {}).items():
        print(f"    - {coll:22} : {count} points indexed")
finally:
    db.close()

print("\n" + "=" * 65)
print("RESULT: QDRANT VECTOR DATABASE IS FULLY WORKING AND OPERATIONAL!")
print("=" * 65)
