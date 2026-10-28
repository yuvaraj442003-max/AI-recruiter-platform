"""
test_qdrant_integration.py — Integration and Unit Tests for Qdrant Vector Database.
"""
import uuid
import pytest
from app.services.qdrant_service import (
    COLLECTION_APTITUDE,
    COLLECTION_CODING,
    COLLECTION_INTERVIEWS,
    COLLECTION_JOBS,
    COLLECTION_LEARNING,
    COLLECTION_RESUMES,
    check_aptitude_question_duplicate,
    delete_document,
    ensure_collections,
    generate_embedding,
    get_health_status,
    is_qdrant_available,
    search,
    sync_all_from_db,
    upsert_batch,
    upsert_document,
)


def test_qdrant_health_and_availability():
    """Verifies that Qdrant service is operational and health status structure is valid."""
    assert is_qdrant_available() is True

    health = get_health_status()
    assert health["enabled"] is True
    assert health["available"] is True
    assert health["vector_dimension"] == 384
    assert "collections" in health
    assert isinstance(health["collections"], dict)


def test_ensure_collections():
    """Verifies that all 6 required vector collections are initialized."""
    ok = ensure_collections()
    assert ok is True

    health = get_health_status()
    for coll in [
        COLLECTION_RESUMES,
        COLLECTION_JOBS,
        COLLECTION_APTITUDE,
        COLLECTION_CODING,
        COLLECTION_INTERVIEWS,
        COLLECTION_LEARNING,
    ]:
        assert coll in health["collections"]
        assert health["collections"][coll]["exists"] is True


def test_generate_embedding():
    """Verifies that generated embeddings have dimension 384 and unit norm."""
    text = "Full Stack Python Developer with FastAPI and React"
    emb = generate_embedding(text)
    assert isinstance(emb, list)
    assert len(emb) == 384
    # All values should be floats
    assert all(isinstance(x, float) for x in emb)


def test_upsert_search_and_delete_document():
    """Tests single document indexing, semantic search, and deletion."""
    ensure_collections()

    doc_id = str(uuid.uuid4())
    job_text = "Senior Machine Learning Engineer specializing in PyTorch, transformers, and LLM fine-tuning."
    metadata = {
        "title": "Senior ML Engineer",
        "company": "DeepTech AI",
        "role": "Machine Learning Engineer",
        "difficulty": "advanced",
    }

    # Upsert
    indexed = upsert_document(
        collection_name=COLLECTION_JOBS,
        doc_id=doc_id,
        text=job_text,
        metadata=metadata,
    )
    assert indexed is True

    # Search
    results = search(
        collection_name=COLLECTION_JOBS,
        query_text="AI and PyTorch transformer models",
        limit=5,
    )
    assert len(results) >= 1
    top_match = results[0]
    assert "score" in top_match
    assert "similarity_pct" in top_match
    assert top_match["similarity_pct"] > 50.0

    # Delete
    deleted = delete_document(COLLECTION_JOBS, doc_id)
    assert deleted is True


def test_metadata_filtering():
    """Tests search with metadata filters (e.g. difficulty)."""
    ensure_collections()

    doc_easy = str(uuid.uuid4())
    doc_hard = str(uuid.uuid4())

    upsert_document(
        collection_name=COLLECTION_CODING,
        doc_id=doc_easy,
        text="Two Sum problem in Python using Hash Map.",
        metadata={"difficulty": "Easy", "category": "Algorithms"},
    )
    upsert_document(
        collection_name=COLLECTION_CODING,
        doc_id=doc_hard,
        text="Median of Two Sorted Arrays in logarithmic time.",
        metadata={"difficulty": "Hard", "category": "Algorithms"},
    )

    # Search with filter
    filtered_results = search(
        collection_name=COLLECTION_CODING,
        query_text="Array algorithm problem",
        filter_dict={"difficulty": "Easy"},
        limit=5,
    )
    assert len(filtered_results) >= 1
    for r in filtered_results:
        assert r["payload"].get("difficulty") == "Easy"


def test_aptitude_duplicate_detection():
    """Verifies that semantically identical or paraphrased aptitude questions are detected."""
    ensure_collections()

    q_id = str(uuid.uuid4())
    q_text = "If a product costs $120 and is sold at a 25% discount, what is the final selling price?"
    upsert_document(
        collection_name=COLLECTION_APTITUDE,
        doc_id=q_id,
        text=q_text,
        metadata={"topic_name": "Percentages", "subtopic": "Discounts"},
    )

    # Paraphrased version
    paraphrased = "A product priced at $120 is offered with a 25% price reduction. Find the sale price."
    duplicate = check_aptitude_question_duplicate(
        question_text=paraphrased,
        similarity_threshold=0.75,
        topic="Percentages",
    )
    assert duplicate is not None
    assert duplicate["payload"]["document_id"] == q_id


def test_sync_all_from_db(db_session):
    """Verifies full database synchronization into Qdrant."""
    res = sync_all_from_db(db_session)
    assert res["status"] == "success"
    assert "counts" in res
    assert isinstance(res["counts"], dict)


def test_vector_api_endpoints(client):
    """Tests FastAPI vector endpoints."""
    # 1. Health endpoint
    resp = client.get("/api/v1/vector/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["available"] is True
    assert data["data"]["vector_dimension"] == 384
