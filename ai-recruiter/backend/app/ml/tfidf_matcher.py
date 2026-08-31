"""
tfidf_matcher.py — lexical similarity between two texts (resume vs job
description) using scikit-learn's TfidfVectorizer + cosine_similarity.

A fresh vectorizer is fit per-comparison (on just the two documents).
This is deliberate: fitting a corpus-wide vectorizer would require
retraining as jobs/resumes are added, which is unnecessary complexity
for a pairwise comparison — TF-IDF over exactly the two documents being
compared is exactly what the spec's "Resume vs Job Description" example
describes.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tfidf_similarity(text_a: str, text_b: str) -> float:
    """Returns a 0-100 lexical similarity score between two texts."""
    text_a = (text_a or "").strip()
    text_b = (text_b or "").strip()
    if not text_a or not text_b:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        matrix = vectorizer.fit_transform([text_a, text_b])
        score = cosine_similarity(matrix[0], matrix[1])[0][0]
    except ValueError:
        # e.g. both documents are entirely stopwords -> empty vocabulary
        return 0.0

    return round(max(0.0, min(1.0, float(score))) * 100, 2)
