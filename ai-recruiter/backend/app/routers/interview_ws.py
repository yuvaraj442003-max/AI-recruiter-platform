"""
interview_ws.py — Real-Time WebSocket router for Live AI Voice Interviews.
Handles bidirectional streaming of candidate audio, live STT transcripts,
adaptive AI question generation, TTS audio playback, and session control.
"""
import base64
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_token
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.interview import Interview, InterviewStatus
from app.models.job import Job, JobSkill
from app.models.user import User
from app.services.live_interview_service import (
    evaluate_completed_live_interview,
    generate_initial_ai_greeting,
    generate_next_ai_turn,
)
from app.services.stt_service import SpeechToTextService

logger = logging.getLogger("ai_recruiter.interview_ws")

router = APIRouter(prefix="/ws", tags=["Live AI Voice Interview WebSockets"])


class ConnectionManager:
    """Manages active WebSocket connections per interview session."""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.dialogue_histories: Dict[str, List[Dict[str, str]]] = {}
        self.question_counts: Dict[str, int] = {}

    async def connect(self, interview_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[interview_id] = websocket
        if interview_id not in self.dialogue_histories:
            self.dialogue_histories[interview_id] = []
        if interview_id not in self.question_counts:
            self.question_counts[interview_id] = 1

    def disconnect(self, interview_id: str):
        self.active_connections.pop(interview_id, None)

    async def send_json(self, interview_id: str, message: dict):
        ws = self.active_connections.get(interview_id)
        if ws:
            await ws.send_json(message)


manager = ConnectionManager()


@router.websocket("/interviews/{interview_id}")
async def interview_websocket_endpoint(websocket: WebSocket, interview_id: str, token: Optional[str] = None):
    """
    WebSocket endpoint for real-time live AI voice interview.
    Requires token query parameter (e.g. /ws/interviews/{id}?token=JWT_TOKEN).
    """
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Authenticate token
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = payload.get("sub")
    db: Session = SessionLocal()

    try:
        # Load interview & candidate
        try:
            int_uuid = uuid.UUID(interview_id)
        except ValueError:
            await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
            return

        interview = db.scalar(select(Interview).where(Interview.id == int_uuid))
        if not interview:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        cand = db.scalar(select(CandidateProfile).where(CandidateProfile.id == interview.candidate_id))
        job = db.scalar(select(Job).where(Job.id == interview.job_id))
        cand_user = db.scalar(select(User).where(User.id == cand.user_id)) if cand else None

        cand_name = cand_user.name if cand_user else "Candidate"
        job_title = job.title if job else "Position"

        await manager.connect(interview_id, websocket)

        # Update interview status to in_progress if scheduled
        if interview.status == InterviewStatus.scheduled:
            interview.status = InterviewStatus.in_progress
            interview.started_at = datetime.now(timezone.utc)
            db.commit()

        # Send initial session state
        await manager.send_json(interview_id, {
            "type": "session.state",
            "state": "CONNECTED",
            "interview_id": interview_id,
            "job_title": job_title,
            "candidate_name": cand_name,
            "duration_minutes": interview.duration_minutes or 30
        })

        while True:
            raw_data = await websocket.receive_text()
            try:
                event = json.loads(raw_data)
            except Exception:
                continue

            event_type = event.get("type")

            # 1. Client Ready / Start Interview
            if event_type == "client.ready":
                greeting_res = generate_initial_ai_greeting(cand_name, job_title)
                manager.dialogue_histories[interview_id].append({
                    "speaker": "AI",
                    "text": greeting_res["text"]
                })
                await manager.send_json(interview_id, {
                    "type": "ai.response",
                    "state": "AI_SPEAKING",
                    "text": greeting_res["text"],
                    "audio_base64": greeting_res["audio_base64"],
                    "format": greeting_res["format"],
                    "provider": greeting_res["provider"],
                    "question_number": 1
                })

            # 2. Candidate Audio Input
            elif event_type == "candidate.audio":
                audio_b64 = event.get("audio_base64")
                if audio_b64:
                    try:
                        audio_bytes = base64.b64decode(audio_b64)
                        stt_res = SpeechToTextService.transcribe(audio_bytes, filename="candidate.webm")
                        transcript = stt_res["text"]
                    except Exception as stt_err:
                        await manager.send_json(interview_id, {
                            "type": "error",
                            "message": f"Transcription notice: {str(stt_err)}. Please type your answer if mic audio was unclear."
                        })
                        continue

                    # Send transcript back to client
                    await manager.send_json(interview_id, {
                        "type": "candidate.transcript",
                        "text": transcript
                    })

                    # Add to history
                    manager.dialogue_histories[interview_id].append({
                        "speaker": "Candidate",
                        "text": transcript
                    })

                    # Notify client AI is analyzing & generating next question
                    await manager.send_json(interview_id, {"type": "ai.processing", "state": "ANALYZING"})

                    # Generate Next AI Turn
                    current_q = manager.question_counts[interview_id] + 1
                    manager.question_counts[interview_id] = current_q

                    cand_skills = [s.skill.name for s in cand.candidate_skills] if cand else []
                    job_skills = [s.skill.name for s in job.job_skills] if job else []

                    ai_turn = generate_next_ai_turn(
                        candidate_name=cand_name,
                        job_title=job_title,
                        job_description=job.description if job else "",
                        required_skills=job_skills,
                        candidate_skills=cand_skills,
                        resume_summary=cand.summary if cand else "",
                        dialogue_history=manager.dialogue_histories[interview_id],
                        interview_type=interview.interview_type.value,
                        current_question_index=current_q,
                        max_questions=8
                    )

                    manager.dialogue_histories[interview_id].append({
                        "speaker": "AI",
                        "text": ai_turn["text"]
                    })

                    await manager.send_json(interview_id, {
                        "type": "ai.response",
                        "state": "AI_SPEAKING",
                        "text": ai_turn["text"],
                        "audio_base64": ai_turn["audio_base64"],
                        "format": ai_turn["format"],
                        "provider": ai_turn["provider"],
                        "question_number": current_q
                    })

            # 3. Candidate Text Answer (Fallback or typed response)
            elif event_type == "candidate.text_answer":
                text_ans = event.get("text", "").strip()
                if text_ans:
                    manager.dialogue_histories[interview_id].append({
                        "speaker": "Candidate",
                        "text": text_ans
                    })

                    await manager.send_json(interview_id, {"type": "ai.processing", "state": "ANALYZING"})

                    current_q = manager.question_counts[interview_id] + 1
                    manager.question_counts[interview_id] = current_q

                    cand_skills = [s.skill.name for s in cand.candidate_skills] if cand else []
                    job_skills = [s.skill.name for s in job.job_skills] if job else []

                    ai_turn = generate_next_ai_turn(
                        candidate_name=cand_name,
                        job_title=job_title,
                        job_description=job.description if job else "",
                        required_skills=job_skills,
                        candidate_skills=cand_skills,
                        resume_summary=cand.summary if cand else "",
                        dialogue_history=manager.dialogue_histories[interview_id],
                        interview_type=interview.interview_type.value,
                        current_question_index=current_q,
                        max_questions=8
                    )

                    manager.dialogue_histories[interview_id].append({
                        "speaker": "AI",
                        "text": ai_turn["text"]
                    })

                    await manager.send_json(interview_id, {
                        "type": "ai.response",
                        "state": "AI_SPEAKING",
                        "text": ai_turn["text"],
                        "audio_base64": ai_turn["audio_base64"],
                        "format": ai_turn["format"],
                        "provider": ai_turn["provider"],
                        "question_number": current_q
                    })

            # 4. End Interview Request
            elif event_type == "interview.end":
                await manager.send_json(interview_id, {"type": "session.state", "state": "EVALUATING"})

                eval_res = evaluate_completed_live_interview(
                    db,
                    int_uuid,
                    manager.dialogue_histories[interview_id]
                )

                await manager.send_json(interview_id, {
                    "type": "interview.completed",
                    "state": "COMPLETED",
                    "overall_score": eval_res.get("overall_score"),
                    "report_url": f"interview-report.html?interview_id={interview_id}"
                })
                break

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected for interview %s", interview_id)
    except Exception as err:
        logger.exception("WebSocket error in interview %s: %s", interview_id, err)
    finally:
        manager.disconnect(interview_id)
        db.close()
