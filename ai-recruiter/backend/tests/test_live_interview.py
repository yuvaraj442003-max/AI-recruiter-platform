"""
test_live_interview.py — Unit and integration tests for the Live AI Voice Interview System:
- TTS service speech generation
- STT service abstraction
- Initial AI greeting and adaptive turn generation
- Live interview evaluation & composite scoring
"""
import pytest
from app.services.live_interview_service import (
    evaluate_completed_live_interview,
    generate_initial_ai_greeting,
    generate_next_ai_turn,
)
from app.services.stt_service import SpeechToTextService
from app.services.tts_service import generate_speech, is_tts_configured


def test_tts_service_response():
    """Test TTS synthesis returns envelope with format and text."""
    res = generate_speech("Hello candidate, welcome to your AI interview.")
    assert res is not None
    assert "format" in res
    assert res["text"] == "Hello candidate, welcome to your AI interview."


def test_stt_service_available():
    """Test STT service status check."""
    status = SpeechToTextService.is_available()
    assert isinstance(status, bool)


def test_generate_initial_ai_greeting():
    """Test initial AI greeting generator."""
    greeting = generate_initial_ai_greeting("John Doe", "Python Developer")
    assert "John Doe" in greeting["text"]
    assert "Python Developer" in greeting["text"]
    assert greeting["question_number"] == 1


def test_generate_next_ai_turn_adaptive():
    """Test adaptive LLM follow-up turn generator."""
    history = [
        {"speaker": "AI", "text": "Tell me about your Python experience."},
        {"speaker": "Candidate", "text": "I have 3 years of Python and FastAPI experience building high-throughput APIs."}
    ]
    turn = generate_next_ai_turn(
        candidate_name="John",
        job_title="Backend Engineer",
        job_description="Python, FastAPI, PostgreSQL",
        required_skills=["Python", "FastAPI"],
        candidate_skills=["Python", "FastAPI", "Docker"],
        resume_summary="Experienced Python developer",
        dialogue_history=history,
        current_question_index=1
    )
    assert turn is not None
    assert "text" in turn
    assert len(turn["text"]) > 10
