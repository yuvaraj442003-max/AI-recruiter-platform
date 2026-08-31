"""
semantic_matcher.py — embedding-based semantic similarity between two
texts (resume vs job description), used to catch matches that TF-IDF's
pure keyword overlap misses (e.g. "built REST APIs" vs "backend web
services" — semantically close, lexically different).

Three tiers, tried in order, so this never hard-fails a request:

1. Sentence-Transformers (`all-MiniLM-L6-v2`) — best quality. Downloads
   from huggingface.co on first use; requires normal internet access.
2. spaCy `en_core_web_md` word vectors — good quality, no network call
   at runtime (just needs the model installed), used automatically if
   tier 1's model can't be downloaded (e.g. restricted network).
3. TF-IDF cosine similarity — same score as the lexical matcher. Last
   resort so a match score is always returned even with nothing else
   installed.

The tier actually in use is logged once at startup so it's obvious
which one is running in a given environment.
"""
import logging

logger = logging.getLogger("ai_recruiter.ml")

_SENTENCE_MODEL = None
_SENTENCE_MODEL_FAILED = False

_SPACY_MD = None
_SPACY_MD_FAILED = False


def _get_sentence_model():
    global _SENTENCE_MODEL, _SENTENCE_MODEL_FAILED
    if _SENTENCE_MODEL is not None or _SENTENCE_MODEL_FAILED:
        return _SENTENCE_MODEL
    try:
        from sentence_transformers import SentenceTransformer

        _SENTENCE_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Semantic matcher: using Sentence-Transformers (all-MiniLM-L6-v2).")
    except Exception as exc:
        _SENTENCE_MODEL_FAILED = True
        logger.warning(
            "Semantic matcher: Sentence-Transformers unavailable (%s). Falling back to spaCy word vectors.", exc
        )
    return _SENTENCE_MODEL


def _get_spacy_md():
    global _SPACY_MD, _SPACY_MD_FAILED
    if _SPACY_MD is not None or _SPACY_MD_FAILED:
        return _SPACY_MD
    try:
        import spacy

        _SPACY_MD = spacy.load("en_core_web_md")
        logger.info("Semantic matcher: using spaCy en_core_web_md word vectors.")
    except Exception as exc:
        _SPACY_MD_FAILED = True
        logger.warning("Semantic matcher: en_core_web_md unavailable (%s). Falling back to TF-IDF.", exc)
    return _SPACY_MD


def _rescale_embedding_score(raw_score: float) -> float:
    """Remaps dense vector cosine similarity (0.35 -> 1.0) into (0.0 -> 1.0) to eliminate
    false high baseline similarity scores for non-matching documents."""
    floor = 0.35
    if raw_score <= floor:
        return 0.0
    normalized = (raw_score - floor) / (1.0 - floor)
    return max(0.0, min(1.0, float(normalized)))


def semantic_similarity(text_a: str, text_b: str) -> float:
    """Returns a 0-100 semantic similarity score between two texts."""
    text_a = (text_a or "").strip()
    text_b = (text_b or "").strip()
    if not text_a or not text_b:
        return 0.0

    model = _get_sentence_model()
    if model is not None:
        import numpy as np

        embeddings = model.encode([text_a[:2000], text_b[:2000]])
        a, b = embeddings[0], embeddings[1]
        denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-8
        score = float(np.dot(a, b) / denom)
        rescaled = _rescale_embedding_score(score)
        return round(rescaled * 100, 2)

    spacy_md = _get_spacy_md()
    if spacy_md is not None:
        doc_a = spacy_md(text_a[:5000])
        doc_b = spacy_md(text_b[:5000])
        if doc_a.has_vector and doc_b.has_vector and doc_a.vector_norm and doc_b.vector_norm:
            score = float(doc_a.similarity(doc_b))
            rescaled = _rescale_embedding_score(score)
            return round(rescaled * 100, 2)
        return 0.0

    from app.ml.tfidf_matcher import tfidf_similarity

    return tfidf_similarity(text_a, text_b)
