"""
llm_service.py — a small, provider-agnostic wrapper around whichever
LLM backend is configured (OpenAI's chat completions API, or the
Hugging Face Inference API). This is the *only* place in the codebase
that knows how to talk to an LLM provider; everything else in app/ai/
calls `generate()` and never touches an API directly, so swapping
providers means changing environment variables, not code.

Configuration (see .env.example):
    LLM_PROVIDER=openai|huggingface   (auto-detected from the keys below if unset)
    OPENAI_API_KEY / OPENAI_MODEL / OPENAI_BASE_URL
    HF_API_KEY / HF_MODEL

If no provider is configured, or the call fails for any reason (no
network, invalid key, rate limit, timeout), `generate()` returns None
rather than raising — every caller in app/ai/ is expected to fall back
to a deterministic, template-based result built from the NLP data we
already have (Phase 2/3). This keeps the feature usable even with no
LLM configured, and keeps a single bad API call from breaking an
unrelated request like an upload or a job posting.
"""
import logging
from typing import Optional

import httpx

from app.core.config import settings

logger = logging.getLogger("ai_recruiter.llm")

_REQUEST_TIMEOUT_SECONDS = 10.0


def get_active_provider() -> Optional[str]:
    """Returns 'gemini', 'openai', 'huggingface', or None if nothing is configured."""
    if settings.LLM_PROVIDER:
        return settings.LLM_PROVIDER.lower()
    if settings.GEMINI_API_KEY:
        return "gemini"
    if settings.OPENAI_API_KEY:
        return "openai"
    if settings.HF_API_KEY:
        return "huggingface"
    if settings.LLM_API_KEY:
        return "gemini" if "AIza" in settings.LLM_API_KEY else "openai"
    return None


def is_configured() -> bool:
    return get_active_provider() is not None


def _call_gemini(system_prompt: str, user_prompt: str, max_tokens: int) -> Optional[str]:
    api_key = settings.GEMINI_API_KEY or settings.LLM_API_KEY
    primary_model = settings.GEMINI_MODEL or settings.LLM_MODEL or "gemini-1.5-flash"

    if not api_key or not api_key.startswith("AIza"):
        logger.debug("No valid Gemini API key configured (key must start with 'AIza'), using template summary output.")
        return None

    # Model candidates to try if 404 or model not found occurs
    models_to_try = [primary_model]
    for fallback in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]:
        if fallback not in models_to_try:
            models_to_try.append(fallback)

    for model in models_to_try:
        try:
            url = f"{settings.GEMINI_BASE_URL}/models/{model}:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [{"text": user_prompt}]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.3,
                }
            }
            if system_prompt:
                payload["systemInstruction"] = {
                    "parts": [{"text": system_prompt}]
                }

            response = httpx.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=_REQUEST_TIMEOUT_SECONDS,
            )
            if response.status_code == 404:
                logger.info("Gemini model '%s' returned 404, trying fallback...", model)
                continue

            response.raise_for_status()
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
            return None
        except Exception as exc:
            logger.warning("Gemini AI call failed on model '%s': %s", model, exc)
            if model == models_to_try[-1]:
                return None
    return None


def _call_openai(system_prompt: str, user_prompt: str, max_tokens: int) -> Optional[str]:
    api_key = settings.OPENAI_API_KEY or settings.LLM_API_KEY
    model = settings.OPENAI_MODEL or settings.LLM_MODEL or "gpt-4o-mini"

    try:
        response = httpx.post(
            f"{settings.OPENAI_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3,
            },
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        logger.warning("OpenAI call failed, falling back to template output: %s", exc)
        return None


def _call_huggingface(system_prompt: str, user_prompt: str, max_tokens: int) -> Optional[str]:
    api_key = settings.HF_API_KEY
    model = settings.HF_MODEL or settings.LLM_MODEL

    try:
        response = httpx.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "inputs": f"{system_prompt}\n\n{user_prompt}",
                "parameters": {"max_new_tokens": max_tokens, "temperature": 0.3},
            },
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
        return None
    except Exception as exc:
        logger.warning("Hugging Face call failed, falling back to template output: %s", exc)
        return None


def generate(system_prompt: str, user_prompt: str, max_tokens: int = 500) -> Optional[str]:
    """
    Calls the configured LLM provider. Returns the raw text response,
    or None if nothing is configured or the call failed — callers must
    handle the None case with a template-based fallback.
    """
    provider = get_active_provider()
    if provider is None:
        logger.info("No LLM provider configured; caller should use its template fallback.")
        return None

    if provider == "gemini":
        return _call_gemini(system_prompt, user_prompt, max_tokens)
    if provider == "openai":
        return _call_openai(system_prompt, user_prompt, max_tokens)
    if provider == "huggingface":
        return _call_huggingface(system_prompt, user_prompt, max_tokens)

    logger.warning("Unknown LLM_PROVIDER '%s'; caller should use its template fallback.", provider)
    return None
