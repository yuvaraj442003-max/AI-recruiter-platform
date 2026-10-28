"""
vector.py — Pydantic schemas for Qdrant vector database operations.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VectorHealthResponse(BaseModel):
    enabled: bool
    available: bool
    mode: str
    remote_url: Optional[str] = None
    storage_path: Optional[str] = None
    embedding_model: str
    vector_dimension: int
    collections: Dict[str, Any] = Field(default_factory=dict)


class VectorSearchRequest(BaseModel):
    collection: str = Field(..., description="Target collection name: resumes, jobs, aptitude_questions, coding_problems, interview_questions, learning_resources")
    query: str = Field(..., min_length=1, description="Natural language search text")
    limit: int = Field(default=10, ge=1, le=100)
    score_threshold: Optional[float] = Field(default=None, ge=-1.0, le=1.0)
    filter: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata filter dictionary")


class VectorSearchResultItem(BaseModel):
    id: str
    score: float
    similarity_pct: float
    payload: Dict[str, Any] = Field(default_factory=dict)


class VectorSearchResponse(BaseModel):
    collection: str
    query: str
    total_found: int
    results: List[VectorSearchResultItem] = Field(default_factory=list)


class VectorSyncResponse(BaseModel):
    status: str
    message: str
    counts: Dict[str, int] = Field(default_factory=dict)


class VectorDuplicateCheckRequest(BaseModel):
    collection: str = Field(default="aptitude_questions", description="Target collection to check for duplicates")
    text: str = Field(..., min_length=3, description="Question or document text to check")
    threshold: float = Field(default=0.88, ge=0.0, le=1.0, description="Cosine similarity duplicate threshold")
    topic: Optional[str] = Field(default=None, description="Optional topic filter to restrict search scope")


class VectorDuplicateCheckResponse(BaseModel):
    is_duplicate: bool
    highest_similarity: float
    duplicate_document: Optional[Dict[str, Any]] = None
