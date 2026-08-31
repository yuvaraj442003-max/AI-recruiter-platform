"""
whisper_service.py — converts a candidate's spoken answer (audio) to
text. Uses OpenAI's Whisper transcription API when an OpenAI key is
configured. There is deliberately no offline/fake fallback here: unlike
summaries or match scores, a transcription that isn't the candidate's
actual words would be actively misleading, not just lower-fidelity — so
if no provider is available, this raises a clear error asking the
candidate to type their answer instead, rather than returning anything.

Per the platform's privacy requirements, audio bytes are only held in
memory for the duration of the request and are never written to disk.
"""
import logging

import httpx

from app.core.config import settings
from app.core.exceptions import AppError

logger = logging.getLogger("ai_recruiter.whisper")

_REQUEST_TIMEOUT_SECONDS = 30.0
_MAX_AUDIO_SIZE_MB = 25


class TranscriptionUnavailableError(AppError):
    def __init__(
        self,
        message: str = "Speech-to-text isn't currently available. Please type your answer instead.",
    ):
        super().__init__(message, "TRANSCRIPTION_UNAVAILABLE", 503)


class TranscriptionFailedError(AppError):
    def __init__(self, message: str = "Could not transcribe this audio. Please try again or type your answer."):
        super().__init__(message, "TRANSCRIPTION_FAILED", 422)


def is_configured() -> bool:
    return bool(settings.OPENAI_API_KEY or settings.LLM_API_KEY)


def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    if len(audio_bytes) > _MAX_AUDIO_SIZE_MB * 1024 * 1024:
        raise AppError(f"Audio file is too large. Maximum size is {_MAX_AUDIO_SIZE_MB}MB.", "FILE_TOO_LARGE", 400)
    if not audio_bytes:
        raise AppError("Audio file is empty.", "EMPTY_FILE", 400)

    if not is_configured():
        logger.info("No Whisper/OpenAI provider configured; transcription unavailable.")
        raise TranscriptionUnavailableError()

    api_key = settings.OPENAI_API_KEY or settings.LLM_API_KEY

    try:
        response = httpx.post(
            f"{settings.OPENAI_BASE_URL}/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (filename, audio_bytes)},
            data={"model": "whisper-1"},
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("text", "").strip()
        if not text:
            raise TranscriptionFailedError()
        return text
    except TranscriptionFailedError:
        raise
    except Exception as exc:
        logger.warning("Whisper transcription failed: %s", exc)
        raise TranscriptionFailedError() from exc
