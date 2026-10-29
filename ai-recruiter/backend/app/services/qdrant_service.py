"""
qdrant_service.py — Production-Grade Vector Database Integration using Qdrant.

Provides semantic search, similarity retrieval, and vector synchronization for:
- Resumes & candidate profiles
- Job descriptions
- Aptitude & reasoning question banks (with duplicate detection)
- Coding problems & algorithmic challenges
- Interview question banks
- Study materials & learning roadmap resources

Design Principles:
1. Resilient & Non-Blocking: Gracefully handles Qdrant connection errors, network restrictions,
   and embedding model loading without interrupting relational database workflows.
2. Dual Deployment Support:
   - Remote/Docker server via QDRANT_URL (e.g. http://localhost:6333 or Qdrant Cloud)
   - Embedded local disk storage via QDRANT_STORAGE_PATH (./qdrant_storage)
   - Transparent in-memory fallback (:memory:) if disk locking or permissions fail.
3. Strict Metadata Filtering: Topic, difficulty, role, company, and content type.
4. Clean Separation: Original relational records stay in PostgreSQL; Qdrant holds
   embeddings, identifiers, and retrieval metadata.
"""
import hashlib
import logging
import math
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from app.core.config import settings

logger = logging.getLogger("ai_recruiter.qdrant")

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.exceptions import UnexpectedResponse
    QDRANT_CLIENT_AVAILABLE = True
except ImportError:
    QdrantClient = None
    models = None
    UnexpectedResponse = Exception
    QDRANT_CLIENT_AVAILABLE = False
    logger.warning("qdrant-client is not installed. Qdrant vector services will run in mock/disabled mode.")

# --- Vector Database Configurations ---
VECTOR_DIMENSION = 384  # Standard dimension for sentence-transformers/all-MiniLM-L6-v2
COLLECTION_RESUMES = "resumes"
COLLECTION_JOBS = "jobs"
COLLECTION_APTITUDE = "aptitude_questions"
COLLECTION_APTITUDE_BOOK = "aptitude_book_knowledge"
COLLECTION_CODING = "coding_problems"
COLLECTION_INTERVIEWS = "interview_questions"
COLLECTION_LEARNING = "learning_resources"

ALL_COLLECTIONS = [
    COLLECTION_RESUMES,
    COLLECTION_JOBS,
    COLLECTION_APTITUDE,
    COLLECTION_APTITUDE_BOOK,
    COLLECTION_CODING,
    COLLECTION_INTERVIEWS,
    COLLECTION_LEARNING,
]

_QDRANT_CLIENT: Optional[Any] = None
_QDRANT_INITIALIZED: bool = False
_SENTENCE_MODEL_INSTANCE: Optional[Any] = None
_SENTENCE_MODEL_TRIED: bool = False


# ---------------------------------------------------------------------------
# Embedding Generation Layer
# ---------------------------------------------------------------------------

def _get_sentence_transformer():
    """Lazily loads the sentence-transformers model with graceful fallback."""
    global _SENTENCE_MODEL_INSTANCE, _SENTENCE_MODEL_TRIED
    if _SENTENCE_MODEL_TRIED:
        return _SENTENCE_MODEL_INSTANCE

    _SENTENCE_MODEL_TRIED = True
    try:
        from sentence_transformers import SentenceTransformer
        model_name = getattr(settings, "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _SENTENCE_MODEL_INSTANCE = SentenceTransformer(model_name)
        logger.info("Qdrant: SentenceTransformer embedding model (%s) loaded successfully.", model_name)
    except Exception as exc:
        _SENTENCE_MODEL_INSTANCE = None
        logger.warning(
            "Qdrant: SentenceTransformer could not be loaded (%s). Using fallback 384-dim semantic projection.",
            exc,
        )
    return _SENTENCE_MODEL_INSTANCE


def _generate_fallback_embedding(text: str, dim: int = VECTOR_DIMENSION) -> List[float]:
    """
    Deterministic 384-dimensional normalized vector projection for environments where
    PyTorch/HuggingFace is offline or restricted. Ensures cosine distance remains mathematically valid.
    """
    words = [w.lower().strip() for w in text.split() if w.strip()]
    vec = [0.0] * dim

    if not words:
        vec[0] = 1.0
        return vec

    for i, word in enumerate(words):
        h = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        # Position-weighted directional signal
        sign = 1.0 if ((h >> 8) & 1) else -1.0
        weight = 1.0 / (math.log(i + 2) + 0.1)
        vec[idx] += sign * weight

    # Normalize to unit length
    norm = math.sqrt(sum(x * x for x in vec)) or 1e-8
    return [round(x / norm, 6) for x in vec]


def generate_embedding(text: str) -> List[float]:
    """Generates a normalized 384-dimensional vector embedding for the input text."""
    clean_text = (text or "").strip()
    if not clean_text:
        vec = [0.0] * VECTOR_DIMENSION
        vec[0] = 1.0
        return vec

    # Try sentence-transformers first
    model = _get_sentence_transformer()
    if model is not None:
        try:
            truncated = clean_text[:2000]
            emb = model.encode(truncated, normalize_embeddings=True)
            return [float(x) for x in emb.tolist()]
        except Exception as err:
            logger.debug("SentenceTransformer encoding failed (%s). Using fallback projection.", err)

    return _generate_fallback_embedding(clean_text, dim=VECTOR_DIMENSION)


def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """Batch generates embeddings efficiently."""
    if not texts:
        return []

    model = _get_sentence_transformer()
    if model is not None:
        try:
            truncated_texts = [(t or "")[:2000] for t in texts]
            embeddings = model.encode(truncated_texts, normalize_embeddings=True, batch_size=32)
            return [[float(x) for x in row.tolist()] for row in embeddings]
        except Exception as err:
            logger.debug("Batch SentenceTransformer encoding failed (%s). Falling back.", err)

    return [generate_embedding(t) for t in texts]


# ---------------------------------------------------------------------------
# Qdrant Client Management
# ---------------------------------------------------------------------------

def _to_qdrant_id(doc_id: Union[str, uuid.UUID, int]) -> str:
    """Ensures document ID is in a valid UUID format acceptable by Qdrant."""
    if isinstance(doc_id, int):
        return str(uuid.UUID(int=doc_id))
    doc_str = str(doc_id).strip()
    try:
        # Check if already a valid UUID
        return str(uuid.UUID(doc_str))
    except (ValueError, AttributeError):
        # Generate deterministic UUID5 based on DNS namespace
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_str))


def get_qdrant_client() -> Optional[Any]:
    """Returns the active QdrantClient instance, initializing it if necessary."""
    global _QDRANT_CLIENT, _QDRANT_INITIALIZED
    if _QDRANT_CLIENT is not None:
        return _QDRANT_CLIENT

    if not QDRANT_CLIENT_AVAILABLE:
        return None

    if not getattr(settings, "QDRANT_ENABLED", True):
        return None

    remote_url = getattr(settings, "QDRANT_URL", "").strip()
    api_key = getattr(settings, "QDRANT_API_KEY", "").strip() or None
    storage_path = getattr(settings, "QDRANT_STORAGE_PATH", "./qdrant_storage").strip()

    # 1. Attempt connection to Remote / Docker Qdrant if URL provided
    if remote_url:
        try:
            client = QdrantClient(url=remote_url, api_key=api_key, timeout=5)
            # Ping to verify
            client.get_collections()
            _QDRANT_CLIENT = client
            _QDRANT_INITIALIZED = True
            logger.info("Qdrant: Connected to remote cluster at %s", remote_url)
            return _QDRANT_CLIENT
        except Exception as exc:
            logger.warning(
                "Qdrant: Remote cluster at %s unreachable (%s). Falling back to local storage.",
                remote_url,
                exc,
            )

    # 2. Attempt local persistent storage path
    if storage_path:
        try:
            os.makedirs(storage_path, exist_ok=True)
            client = QdrantClient(path=storage_path)
            _QDRANT_CLIENT = client
            _QDRANT_INITIALIZED = True
            logger.info("Qdrant: Local persistent vector storage initialized at %s", storage_path)
            return _QDRANT_CLIENT
        except Exception as exc:
            logger.warning(
                "Qdrant: Could not open local storage at %s (%s). Falling back to in-memory mode.",
                storage_path,
                exc,
            )

    # 3. Fallback to in-memory Qdrant client
    try:
        client = QdrantClient(":memory:")
        _QDRANT_CLIENT = client
        _QDRANT_INITIALIZED = True
        logger.info("Qdrant: In-memory vector database active.")
        return _QDRANT_CLIENT
    except Exception as exc:
        logger.error("Qdrant: Failed to initialize in-memory vector database: %s", exc)
        return None


def is_qdrant_available() -> bool:
    """Checks whether Qdrant client is operational."""
    client = get_qdrant_client()
    if client is None:
        return False
    try:
        client.get_collections()
        return True
    except Exception:
        return False


def ensure_collections() -> bool:
    """Idempotently ensures all project vector collections exist with cosine distance."""
    client = get_qdrant_client()
    if client is None or models is None:
        return False

    prefix = getattr(settings, "QDRANT_COLLECTION_PREFIX", "")
    success = True

    for base_name in ALL_COLLECTIONS:
        coll_name = f"{prefix}{base_name}"
        try:
            if not client.collection_exists(coll_name):
                client.create_collection(
                    collection_name=coll_name,
                    vectors_config=models.VectorParams(
                        size=VECTOR_DIMENSION,
                        distance=models.Distance.COSINE,
                    ),
                )
                logger.info("Qdrant: Created collection '%s'", coll_name)
        except Exception as exc:
            logger.warning("Qdrant: Could not ensure collection '%s': %s", coll_name, exc)
            success = False

    return success


# ---------------------------------------------------------------------------
# Vector CRUD Operations
# ---------------------------------------------------------------------------

def _get_full_collection_name(base_name: str) -> str:
    prefix = getattr(settings, "QDRANT_COLLECTION_PREFIX", "")
    return f"{prefix}{base_name}"


def upsert_document(
    collection_name: str,
    doc_id: Union[str, uuid.UUID, int],
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
    vector: Optional[List[float]] = None,
) -> bool:
    """
    Upserts a document vector with metadata payload into the specified collection.
    If vector is omitted, it is generated from the text.
    """
    client = get_qdrant_client()
    if client is None or models is None:
        return False

    coll = _get_full_collection_name(collection_name)
    try:
        if not client.collection_exists(coll):
            ensure_collections()

        if vector is None:
            vector = generate_embedding(text)

        payload = dict(metadata or {})
        payload["document_id"] = str(doc_id)
        # Store a snippet of text for preview
        payload["text_snippet"] = (text or "")[:500]

        point = models.PointStruct(
            id=_to_qdrant_id(doc_id),
            vector=vector,
            payload=payload,
        )

        client.upsert(collection_name=coll, points=[point])
        return True
    except Exception as exc:
        logger.warning("Qdrant: Failed to upsert document %s in %s: %s", doc_id, coll, exc)
        return False


def upsert_batch(
    collection_name: str,
    items: List[Dict[str, Any]],
) -> int:
    """
    Upserts a batch of documents into the specified collection.
    Each item must contain 'id' and 'text', and optionally 'metadata' and 'vector'.
    Returns the count of successfully indexed items.
    """
    client = get_qdrant_client()
    if client is None or models is None or not items:
        return 0

    coll = _get_full_collection_name(collection_name)
    try:
        if not client.collection_exists(coll):
            ensure_collections()

        # Generate embeddings for items missing vectors
        texts_to_embed = [item["text"] for item in items if "vector" not in item]
        computed_embeddings = generate_batch_embeddings(texts_to_embed) if texts_to_embed else []
        emb_iter = iter(computed_embeddings)

        points = []
        for item in items:
            doc_id = item["id"]
            text = item.get("text", "")
            vec = item.get("vector")
            if vec is None:
                vec = next(emb_iter)

            payload = dict(item.get("metadata") or {})
            payload["document_id"] = str(doc_id)
            payload["text_snippet"] = text[:500]

            points.append(
                models.PointStruct(
                    id=_to_qdrant_id(doc_id),
                    vector=vec,
                    payload=payload,
                )
            )

        # Batch upsert in chunks of 50
        chunk_size = 50
        total_upserted = 0
        for i in range(0, len(points), chunk_size):
            chunk = points[i : i + chunk_size]
            client.upsert(collection_name=coll, points=chunk)
            total_upserted += len(chunk)

        return total_upserted
    except Exception as exc:
        logger.warning("Qdrant: Batch upsert failed in %s: %s", coll, exc)
        return 0


def delete_document(collection_name: str, doc_id: Union[str, uuid.UUID, int]) -> bool:
    """Deletes a document vector from the specified collection."""
    client = get_qdrant_client()
    if client is None or models is None:
        return False

    coll = _get_full_collection_name(collection_name)
    try:
        if not client.collection_exists(coll):
            return True

        client.delete(
            collection_name=coll,
            points_selector=models.PointIdsList(points=[_to_qdrant_id(doc_id)]),
        )
        return True
    except Exception as exc:
        logger.warning("Qdrant: Failed to delete document %s from %s: %s", doc_id, coll, exc)
        return False


# ---------------------------------------------------------------------------
# Semantic Search & Similarity Retrieval
# ---------------------------------------------------------------------------

def _build_filter(filter_dict: Optional[Dict[str, Any]]) -> Optional[Any]:
    """Converts a key-value dictionary into Qdrant filter conditions."""
    if not filter_dict or models is None:
        return None

    must_conditions = []
    for key, val in filter_dict.items():
        if val is None:
            continue
        if isinstance(val, (list, tuple, set)):
            # Match any in values
            must_conditions.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchAny(any=list(val)),
                )
            )
        else:
            must_conditions.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=val),
                )
            )

    return models.Filter(must=must_conditions) if must_conditions else None


def search(
    collection_name: str,
    query_text: Optional[str] = None,
    query_vector: Optional[List[float]] = None,
    limit: int = 10,
    score_threshold: Optional[float] = None,
    filter_dict: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Performs cosine similarity search against the specified collection.
    Returns ranked list of matching documents with score (0.0 to 1.0) and payload.
    """
    client = get_qdrant_client()
    if client is None or models is None:
        return []

    coll = _get_full_collection_name(collection_name)
    try:
        if not client.collection_exists(coll):
            return []

        if query_vector is None:
            if not query_text:
                return []
            query_vector = generate_embedding(query_text)

        qdrant_filter = _build_filter(filter_dict)

        resp = client.query_points(
            collection_name=coll,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=qdrant_filter,
        )

        results = []
        for point in getattr(resp, "points", []):
            raw_score = float(point.score) if point.score is not None else 0.0
            # Normalize cosine score from [-1, 1] to [0, 1]
            normalized_score = max(0.0, min(1.0, (raw_score + 1.0) / 2.0))
            results.append({
                "id": str(point.id),
                "score": round(raw_score, 4),
                "similarity_pct": round(normalized_score * 100, 2),
                "payload": point.payload or {},
            })

        return results
    except Exception as exc:
        logger.warning("Qdrant: Search query failed on %s: %s", coll, exc)
        return []


def find_similar(
    collection_name: str,
    text: str,
    limit: int = 5,
    score_threshold: float = 0.85,
    filter_dict: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Finds documents highly similar to the provided text above the threshold."""
    return search(
        collection_name=collection_name,
        query_text=text,
        limit=limit,
        score_threshold=score_threshold,
        filter_dict=filter_dict,
    )


def check_aptitude_question_duplicate(
    question_text: str,
    similarity_threshold: float = 0.88,
    topic: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Checks if a question is semantically identical or near-duplicate to an existing question.
    Returns the matching existing question's payload if similarity >= threshold, else None.
    """
    filters = {"topic_name": topic} if topic else None
    matches = find_similar(
        collection_name=COLLECTION_APTITUDE,
        text=question_text,
        limit=1,
        score_threshold=similarity_threshold,
        filter_dict=filters,
    )
    if matches:
        return matches[0]
    return None


# ---------------------------------------------------------------------------
# Database Synchronization & Re-indexing
# ---------------------------------------------------------------------------

def sync_all_from_db(db: Session) -> Dict[str, Any]:
    """
    Safely indexes existing relational database records into Qdrant collections.
    Idempotent: updates existing points without creating duplicates.
    """
    if not ensure_collections():
        return {
            "status": "failed",
            "message": "Qdrant collections could not be ensured or Qdrant is disabled.",
            "counts": {},
        }

    counts = {
        "jobs": 0,
        "resumes": 0,
        "aptitude_questions": 0,
        "coding_problems": 0,
        "interview_questions": 0,
        "learning_resources": 0,
    }

    try:
        # 1. Index Jobs
        from app.models.job import Job
        jobs = db.query(Job).all()
        job_items = []
        for j in jobs:
            skills = [js.skill.skill_name for js in j.job_skills if js.skill] if hasattr(j, "job_skills") else []
            full_text = f"Title: {j.title}\nCompany: {getattr(j, 'company_name', '') or ''}\nSkills: {', '.join(skills)}\nDescription: {j.description}"
            job_items.append({
                "id": str(j.id),
                "text": full_text,
                "metadata": {
                    "job_id": str(j.id),
                    "title": j.title,
                    "company": getattr(j, "company_name", None),
                    "location": j.location,
                    "skills": skills,
                    "status": str(j.status),
                    "experience_required": j.experience_required,
                },
            })
        counts["jobs"] = upsert_batch(COLLECTION_JOBS, job_items)

        # 2. Index Resumes / Candidates
        from app.models.candidate import CandidateProfile
        candidates = db.query(CandidateProfile).all()
        cand_items = []
        for c in candidates:
            skills = [cs.skill.skill_name for cs in c.candidate_skills if cs.skill] if hasattr(c, "candidate_skills") else []
            body = c.resume_text or c.summary or c.headline or ""
            if not body and not skills:
                continue
            full_text = f"Headline: {c.headline or ''}\nSkills: {', '.join(skills)}\nSummary: {c.summary or ''}\nExperience: {c.work_experience or ''}\nResume: {body}"
            cand_items.append({
                "id": str(c.id),
                "text": full_text,
                "metadata": {
                    "candidate_id": str(c.id),
                    "user_id": str(c.user_id),
                    "headline": c.headline,
                    "current_role": c.current_role,
                    "experience_years": c.experience_years,
                    "skills": skills,
                    "college_name": getattr(c, "college_name", None),
                    "target_role": getattr(c, "target_role", None),
                },
            })
        counts["resumes"] = upsert_batch(COLLECTION_RESUMES, cand_items)

        # 3. Index Aptitude Questions
        from app.models.student import AptitudeQuestion
        apt_questions = db.query(AptitudeQuestion).all()
        apt_items = []
        for aq in apt_questions:
            topic_str = aq.topic_name or (aq.topic.name if aq.topic else "")
            full_text = f"Topic: {topic_str}\nSubtopic: {aq.subtopic}\nQuestion: {aq.question}"
            apt_items.append({
                "id": str(aq.id),
                "text": full_text,
                "metadata": {
                    "question_id": str(aq.id),
                    "topic_name": topic_str,
                    "subtopic": aq.subtopic,
                    "difficulty": aq.difficulty,
                    "company_tag": aq.company_tag,
                },
            })
        counts["aptitude_questions"] = upsert_batch(COLLECTION_APTITUDE, apt_items)

        # 4. Index Coding Problems
        from app.models.coding import CodingQuestion
        coding_questions = db.query(CodingQuestion).all()
        coding_items = []
        for cq in coding_questions:
            full_text = f"Title: {cq.title}\nCategory: {cq.category}\nDifficulty: {cq.difficulty}\nDescription: {cq.description}"
            coding_items.append({
                "id": str(cq.id),
                "text": full_text,
                "metadata": {
                    "problem_id": str(cq.id),
                    "title": cq.title,
                    "category": cq.category,
                    "difficulty": cq.difficulty,
                    "status": cq.status,
                },
            })
        counts["coding_problems"] = upsert_batch(COLLECTION_CODING, coding_items)

        # 5. Index Interview Questions
        from app.models.interview import InterviewQuestion
        interview_questions = db.query(InterviewQuestion).all()
        interview_items = []
        for iq in interview_questions:
            full_text = f"Type: {iq.question_type}\nDifficulty: {iq.difficulty}\nQuestion: {iq.question}"
            interview_items.append({
                "id": str(iq.id),
                "text": full_text,
                "metadata": {
                    "question_id": str(iq.id),
                    "question_type": iq.question_type,
                    "difficulty": iq.difficulty,
                },
            })
        counts["interview_questions"] = upsert_batch(COLLECTION_INTERVIEWS, interview_items)

        # 6. Index Study Materials & Roadmaps
        from app.models.student import StudyMaterial
        materials = db.query(StudyMaterial).all()
        material_items = []
        for sm in materials:
            full_text = f"Title: {sm.title}\nCategory: {sm.category}\nDifficulty: {sm.difficulty}\nDescription: {sm.description or ''}\nContent: {sm.content_markdown[:1500]}"
            material_items.append({
                "id": str(sm.id),
                "text": full_text,
                "metadata": {
                    "resource_id": str(sm.id),
                    "title": sm.title,
                    "category": sm.category,
                    "difficulty": sm.difficulty,
                    "content_type": sm.content_type,
                },
            })
        counts["learning_resources"] = upsert_batch(COLLECTION_LEARNING, material_items)

        # 7. Index RS Aggarwal Reasoning PDF textbook knowledge if present
        try:
            from app.services.aptitude_pdf_rag_service import index_reasoning_pdf_to_qdrant
            pdf_idx_res = index_reasoning_pdf_to_qdrant(force=False)
            counts["aptitude_book_knowledge"] = pdf_idx_res.get("points_count", 0)
        except Exception as p_err:
            logger.debug("PDF indexing during sync_all note: %s", p_err)

        return {
            "status": "success",
            "message": "All database entities and textbook knowledge synchronized to Qdrant vector database.",
            "counts": counts,
        }
    except Exception as exc:
        logger.exception("Qdrant synchronization failed: %s", exc)
        return {
            "status": "error",
            "message": str(exc),
            "counts": counts,
        }


# ---------------------------------------------------------------------------
# Health & Status Monitoring
# ---------------------------------------------------------------------------

def get_health_status() -> Dict[str, Any]:
    """Returns diagnostics and statistics for Qdrant service."""
    client = get_qdrant_client()
    prefix = getattr(settings, "QDRANT_COLLECTION_PREFIX", "")

    if client is None:
        return {
            "enabled": getattr(settings, "QDRANT_ENABLED", False),
            "available": False,
            "mode": "disabled_or_unavailable",
            "collections": {},
            "embedding_model": getattr(settings, "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
            "vector_dimension": VECTOR_DIMENSION,
        }

    # Determine mode
    remote_url = getattr(settings, "QDRANT_URL", "").strip()
    storage_path = getattr(settings, "QDRANT_STORAGE_PATH", "").strip()
    if remote_url:
        mode = "remote"
    elif storage_path:
        mode = "local_disk"
    else:
        mode = "in_memory"

    collections_stat = {}
    for base_name in ALL_COLLECTIONS:
        coll_name = f"{prefix}{base_name}"
        try:
            if client.collection_exists(coll_name):
                c_info = client.get_collection(coll_name)
                # Count points
                p_count = client.count(coll_name).count
                collections_stat[base_name] = {
                    "exists": True,
                    "points_count": p_count,
                    "status": str(getattr(c_info, "status", "ready")),
                }
            else:
                collections_stat[base_name] = {
                    "exists": False,
                    "points_count": 0,
                    "status": "not_created",
                }
        except Exception as e:
            collections_stat[base_name] = {
                "exists": False,
                "error": str(e),
            }

    return {
        "enabled": getattr(settings, "QDRANT_ENABLED", True),
        "available": True,
        "mode": mode,
        "remote_url": remote_url or None,
        "storage_path": storage_path if mode == "local_disk" else None,
        "embedding_model": getattr(settings, "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        "vector_dimension": VECTOR_DIMENSION,
        "collections": collections_stat,
    }
