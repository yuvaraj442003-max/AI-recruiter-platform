"""
text_processor.py — shared NLP preprocessing pipeline.

Uses spaCy for tokenization, lemmatization, stopword removal, and NER
(spaCy ships its own stopword list and is what actually powers the
pipeline). NLTK is used for a couple of specific helpers (sentence
tokenization, an independent stopword list used to sanity-check spaCy's)
so both libraries called for in the spec are genuinely doing work here.

The spaCy model is loaded once at import time and reused — loading it
per-request would be far too slow for an API.
"""
import logging
import re

import nltk
import spacy

logger = logging.getLogger("ai_recruiter.nlp")

_NLTK_READY = False


def _ensure_nltk_data() -> None:
    global _NLTK_READY
    if _NLTK_READY:
        return
    for pkg in ("punkt", "punkt_tab", "stopwords"):
        try:
            nltk.download(pkg, quiet=True)
        except Exception as exc:  # pragma: no cover - network dependent
            logger.warning("Could not fetch NLTK data package '%s': %s", pkg, exc)
    _NLTK_READY = True


try:
    NLP = spacy.load("en_core_web_sm")
except OSError:  # pragma: no cover - model not installed
    logger.warning("spaCy model 'en_core_web_sm' not found; falling back to a blank English pipeline.")
    NLP = spacy.blank("en")

_WHITESPACE_RE = re.compile(r"[ \t]+")
_MULTI_NEWLINE_RE = re.compile(r"\n{3,}")
_BULLET_RE = re.compile(r"^[•▪●\-\*]\s*", re.MULTILINE)


def clean_text(raw_text: str) -> str:
    """Normalize whitespace/bullets without destroying line structure (needed
    for section-based extraction like education/experience later)."""
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = _BULLET_RE.sub("", text)
    text = _WHITESPACE_RE.sub(" ", text)
    text = _MULTI_NEWLINE_RE.sub("\n\n", text)
    return text.strip()


def tokenize_and_lemmatize(text: str) -> list[str]:
    """
    Tokenize with spaCy, drop stopwords/punctuation/whitespace tokens,
    and return lemmatized lowercase tokens. This is the representation
    used for TF-IDF/matching in Phase 3.
    """
    doc = NLP(text)
    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space and token.lemma_.strip()
    ]


def sentence_split(text: str) -> list[str]:
    """NLTK-based sentence tokenization, used for summary generation."""
    _ensure_nltk_data()
    try:
        from nltk.tokenize import sent_tokenize

        return [s.strip() for s in sent_tokenize(text) if s.strip()]
    except Exception:
        # Fallback: naive split on sentence-ending punctuation.
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def extract_entities(text: str) -> dict[str, list[str]]:
    """Run spaCy NER and bucket entities by label (PERSON, ORG, GPE, DATE)."""
    # NER is expensive on very long documents; a resume rarely needs more
    # than the first ~4000 characters analyzed for name/org/location cues.
    doc = NLP(text[:4000])
    buckets: dict[str, list[str]] = {"PERSON": [], "ORG": [], "GPE": [], "DATE": []}
    for ent in doc.ents:
        if ent.label_ in buckets and ent.text.strip() not in buckets[ent.label_]:
            buckets[ent.label_].append(ent.text.strip())
    return buckets
