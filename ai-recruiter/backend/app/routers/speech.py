"""
Speech-to-text endpoint: transcribes a candidate's voice answer via
Whisper. Generic (not tied to a specific interview/question) so the
candidate can review the transcription before deciding which answer
to submit.
"""
from fastapi import APIRouter, Depends, File, UploadFile

from app.ai.whisper_service import transcribe_audio
from app.core.deps import require_role
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.interview import TranscriptionResponse

router = APIRouter(prefix="/speech", tags=["Speech"])


@router.post("/transcribe", response_model=APIResponse[TranscriptionResponse])
async def transcribe(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.candidate)),
):
    audio_bytes = await file.read()
    text = transcribe_audio(audio_bytes, file.filename or "audio")
    return APIResponse(success=True, message="Audio transcribed", data=TranscriptionResponse(text=text))
