"""
stt_service.py — Speech-to-Text (STT) Service Abstraction.
Wraps OpenAI Whisper / speech transcription and provides structured response envelopes.
"""
import logging
from typing import Any, Dict

from app.ai.whisper_service import is_configured as is_whisper_configured, transcribe_audio

logger = logging.getLogger("ai_recruiter.stt")


class SpeechToTextService:
    @staticmethod
    def is_available() -> bool:
        return is_whisper_configured()

    @staticmethod
    def transcribe(audio_bytes: bytes, filename: str = "recording.webm") -> Dict[str, Any]:
        """
        Transcribes candidate audio bytes to text.
        Returns structured dict:
            {
                "text": str,
                "language": "en",
                "duration": float,
                "provider": "whisper" | "fallback"
            }
        """
        try:
            transcript = transcribe_audio(audio_bytes, filename)
            return {
                "text": transcript,
                "language": "en",
                "duration": round(len(audio_bytes) / 32000.0, 1),  # Estimated duration
                "provider": "whisper"
            }
        except Exception as err:
            logger.warning("STT transcription error: %s", err)
            raise err
