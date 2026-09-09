"""
tts_service.py — Text-to-Speech (TTS) Service Abstraction.
Converts AI interviewer text responses into natural-sounding spoken audio.
Supports OpenAI TTS API (tts-1) with fallback synthesizer metadata for browser WebSpeech API.
"""
import base64
import logging
from typing import Any, Dict, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger("ai_recruiter.tts")

_REQUEST_TIMEOUT_SECONDS = 15.0


def is_tts_configured() -> bool:
    """Check if OpenAI TTS or external API key is configured."""
    return bool(settings.OPENAI_API_KEY or settings.LLM_API_KEY)


def generate_speech(text: str, voice: str = "alloy") -> Dict[str, Any]:
    """
    Synthesizes speech from text.
    Returns:
        {
            "audio_base64": str (base64 encoded MP3 audio data if available),
            "format": "mp3",
            "provider": "openai" | "fallback",
            "text": str
        }
    """
    if not text or not text.strip():
        return {"audio_base64": None, "format": "mp3", "provider": "none", "text": text}

    if is_tts_configured():
        api_key = settings.OPENAI_API_KEY or settings.LLM_API_KEY
        try:
            url = f"{settings.OPENAI_BASE_URL}/audio/speech"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "tts-1",
                "input": text.strip(),
                "voice": voice  # alloy, echo, fable, onyx, nova, shimmer
            }
            response = httpx.post(url, headers=headers, json=payload, timeout=_REQUEST_TIMEOUT_SECONDS)
            if response.status_code == 200:
                audio_b64 = base64.b64encode(response.content).decode("utf-8")
                return {
                    "audio_base64": audio_b64,
                    "format": "mp3",
                    "provider": "openai",
                    "text": text
                }
        except Exception as err:
            logger.warning("OpenAI TTS API call failed: %s. Using browser WebSpeech fallback.", err)

    # Browser WebSpeech fallback indicator
    return {
        "audio_base64": None,
        "format": "webspeech",
        "provider": "browser_webspeech",
        "text": text
    }
