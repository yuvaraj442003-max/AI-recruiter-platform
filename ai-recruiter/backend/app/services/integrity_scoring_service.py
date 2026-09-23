"""
integrity_scoring_service.py — Deterministic Evidence-Based Integrity Scoring Engine.
Computes explainable integrity scores and risk levels based on recorded monitoring events,
vision/audio indicators, and code similarity analysis.
"""
import json
import logging
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.models.coding import CandidateCodingAttempt
from app.models.proctoring import AssessmentEvent, CodeSimilarityResult, EventSeverity, IntegrityResult, RiskLevel

logger = logging.getLogger("ai_recruiter.integrity_scoring")

# Penalty rules for measurable monitoring events
PENALTY_RULES = {
    "TAB_SWITCH": {"deduction": 10.0, "max_deduction": 50.0, "category": "browser"},
    "TAB_RETURN": {"deduction": 0.0, "max_deduction": 0.0, "category": "browser"},
    "WINDOW_BLUR": {"deduction": 5.0, "max_deduction": 30.0, "category": "browser"},
    "WINDOW_FOCUS": {"deduction": 0.0, "max_deduction": 0.0, "category": "browser"},
    "FULLSCREEN_EXIT": {"deduction": 15.0, "max_deduction": 45.0, "category": "browser"},
    "PASTE": {"deduction": 5.0, "max_deduction": 20.0, "category": "browser"},
    "PASTE_ATTEMPT": {"deduction": 5.0, "max_deduction": 20.0, "category": "browser"},
    "COPY_ATTEMPT": {"deduction": 2.0, "max_deduction": 10.0, "category": "browser"},
    "CUT_ATTEMPT": {"deduction": 2.0, "max_deduction": 10.0, "category": "browser"},
    "NO_FACE": {"deduction": 15.0, "max_deduction": 45.0, "category": "webcam"},
    "NO_FACE_DETECTED": {"deduction": 15.0, "max_deduction": 45.0, "category": "webcam"},
    "FACE_DETECTED_AGAIN": {"deduction": 0.0, "max_deduction": 0.0, "category": "webcam"},
    "MULTIPLE_FACES": {"deduction": 25.0, "max_deduction": 50.0, "category": "webcam"},
    "MULTIPLE_FACES_DETECTED": {"deduction": 25.0, "max_deduction": 50.0, "category": "webcam"},
    "FACE_LOST": {"deduction": 10.0, "max_deduction": 30.0, "category": "webcam"},
    "ADDITIONAL_VOICE": {"deduction": 20.0, "max_deduction": 50.0, "category": "audio"},
    "CONTINUOUS_VOICE_ACTIVITY": {"deduction": 10.0, "max_deduction": 30.0, "category": "audio"},
    "HIGH_AUDIO_SPIKE": {"deduction": 5.0, "max_deduction": 25.0, "category": "audio"},
    "MIC_MUTED_OR_DISCONNECTED": {"deduction": 15.0, "max_deduction": 30.0, "category": "audio"},
    "SUSPICIOUS_AUDIO": {"deduction": 10.0, "max_deduction": 30.0, "category": "audio"},
    "NOISE_DETECTED": {"deduction": 10.0, "max_deduction": 30.0, "category": "audio"},
}


def calculate_attempt_integrity(db: Session, attempt_id: str) -> IntegrityResult:
    """
    Calculates sub-scores, overall integrity score, risk level, and evidence summary for an assessment attempt.
    """
    attempt = db.query(CandidateCodingAttempt).filter(CandidateCodingAttempt.id == attempt_id).first()
    if not attempt:
        raise ValueError(f"Candidate attempt {attempt_id} not found.")

    events = db.query(AssessmentEvent).filter(AssessmentEvent.attempt_id == attempt.id).all()
    similarity_records = db.query(CodeSimilarityResult).filter(CodeSimilarityResult.attempt_id == attempt.id).all()

    # Track event counts and total deductions by category
    category_penalties = {"browser": 0.0, "webcam": 0.0, "audio": 0.0}
    event_counts: Dict[str, int] = {}
    evidence_bullets = []

    for ev in events:
        ev_type = ev.event_type.upper()
        event_counts[ev_type] = event_counts.get(ev_type, 0) + 1

        if ev_type in PENALTY_RULES:
            rule = PENALTY_RULES[ev_type]
            cat = rule["category"]
            category_penalties[cat] = min(
                rule["max_deduction"],
                category_penalties[cat] + rule["deduction"]
            )

    # Compile event evidence bullets
    if event_counts.get("TAB_SWITCH", 0) > 0:
        evidence_bullets.append(f"• Tab switches detected: {event_counts['TAB_SWITCH']} event(s).")
    if event_counts.get("FULLSCREEN_EXIT", 0) > 0:
        evidence_bullets.append(f"• Fullscreen mode exited: {event_counts['FULLSCREEN_EXIT']} time(s).")
    if event_counts.get("PASTE", 0) > 0:
        evidence_bullets.append(f"• Clipboard paste activity: {event_counts['PASTE']} event(s).")
    if event_counts.get("MULTIPLE_FACES", 0) > 0:
        evidence_bullets.append(f"• Multiple faces detected on webcam: {event_counts['MULTIPLE_FACES']} event(s).")
    if event_counts.get("NO_FACE", 0) > 0:
        evidence_bullets.append(f"• Face absence detected on camera: {event_counts['NO_FACE']} event(s).")
    if event_counts.get("ADDITIONAL_VOICE", 0) > 0:
        evidence_bullets.append(f"• Additional secondary voice detected on audio stream: {event_counts['ADDITIONAL_VOICE']} event(s).")
    if event_counts.get("SUSPICIOUS_AUDIO", 0) > 0 or event_counts.get("NOISE_DETECTED", 0) > 0:
        audio_events_cnt = event_counts.get("SUSPICIOUS_AUDIO", 0) + event_counts.get("NOISE_DETECTED", 0)
        evidence_bullets.append(f"• External background noise or suspicious audio detected: {audio_events_cnt} event(s).")

    # Compute Sub-Scores (Starting from 100.0)
    browser_score = max(0.0, 100.0 - category_penalties["browser"])
    webcam_score = max(0.0, 100.0 - category_penalties["webcam"])
    audio_score = max(0.0, 100.0 - category_penalties["audio"])

    # Code Similarity Sub-Score
    max_sim = 0.0
    for sim in similarity_records:
        if sim.similarity_score > max_sim:
            max_sim = sim.similarity_score

    if max_sim >= 80.0:
        code_similarity_score = max(20.0, 100.0 - max_sim)
        evidence_bullets.append(f"• High AST code similarity match detected ({max_sim:.1f}% similarity).")
    elif max_sim >= 50.0:
        code_similarity_score = max(50.0, 100.0 - (max_sim * 0.5))
        evidence_bullets.append(f"• Moderate code similarity match detected ({max_sim:.1f}% similarity).")
    else:
        code_similarity_score = 100.0
        evidence_bullets.append(f"• Code similarity check passed (Max match {max_sim:.1f}%).")

    behavior_score = round((browser_score + webcam_score) / 2.0, 1)

    # Weighted Overall Integrity Score
    overall_integrity = round(
        (browser_score * 0.30) +
        (webcam_score * 0.30) +
        (audio_score * 0.20) +
        (code_similarity_score * 0.20),
        1
    )

    # Determine Risk Level Category
    if overall_integrity >= 85.0:
        risk_level = RiskLevel.low_risk
    elif overall_integrity >= 60.0:
        risk_level = RiskLevel.review_recommended
    else:
        risk_level = RiskLevel.high_risk

    # Format AI-Assisted Integrity Summary
    summary_header = (
        f"AI-Assisted Integrity Summary\n"
        f"Overall Integrity Score: {overall_integrity}%\n"
        f"Risk Level: {risk_level.value}\n\n"
        f"Observed Signals:\n"
    )
    if not evidence_bullets:
        evidence_bullets.append("• No suspicious activity or integrity signals recorded during assessment.")

    summary_footer = (
        "\n\nImportant: These signals indicate potential suspicious activity. "
        "They do not guarantee detection of cheating and do not automatically determine hiring outcomes. "
        "Recruiter review is recommended."
    )
    ai_summary_text = summary_header + "\n".join(evidence_bullets) + summary_footer

    # Persist or update IntegrityResult row
    result_obj = db.query(IntegrityResult).filter(IntegrityResult.attempt_id == attempt.id).first()
    if not result_obj:
        result_obj = IntegrityResult(
            attempt_id=attempt.id,
            browser_score=browser_score,
            webcam_score=webcam_score,
            audio_score=audio_score,
            code_similarity_score=code_similarity_score,
            behavior_score=behavior_score,
            overall_integrity_score=overall_integrity,
            risk_level=risk_level,
            ai_summary=ai_summary_text,
        )
        db.add(result_obj)
    else:
        result_obj.browser_score = browser_score
        result_obj.webcam_score = webcam_score
        result_obj.audio_score = audio_score
        result_obj.code_similarity_score = code_similarity_score
        result_obj.behavior_score = behavior_score
        result_obj.overall_integrity_score = overall_integrity
        result_obj.risk_level = risk_level
        result_obj.ai_summary = ai_summary_text

    db.commit()
    db.refresh(result_obj)
    return result_obj


def calculate_interview_integrity(db: Session, interview_id: str) -> IntegrityResult:
    """
    Calculates sub-scores, overall integrity score, risk level, and evidence summary for an AI video interview.
    """
    from app.models.interview import Interview
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise ValueError(f"Interview {interview_id} not found.")

    events = db.query(AssessmentEvent).filter(AssessmentEvent.interview_id == interview.id).all()

    category_penalties = {"browser": 0.0, "webcam": 0.0, "audio": 0.0}
    event_counts: Dict[str, int] = {}
    evidence_bullets = []

    for ev in events:
        ev_type = ev.event_type.upper()
        event_counts[ev_type] = event_counts.get(ev_type, 0) + 1

        if ev_type in PENALTY_RULES:
            rule = PENALTY_RULES[ev_type]
            cat = rule["category"]
            category_penalties[cat] = min(
                rule["max_deduction"],
                category_penalties[cat] + rule["deduction"]
            )

    # Compile event evidence bullets
    if event_counts.get("TAB_SWITCH", 0) > 0:
        evidence_bullets.append(f"• Tab switches detected: {event_counts['TAB_SWITCH']} event(s).")
    if event_counts.get("WINDOW_BLUR", 0) > 0:
        evidence_bullets.append(f"• Window focus lost: {event_counts['WINDOW_BLUR']} event(s).")
    if event_counts.get("MULTIPLE_FACES_DETECTED", 0) > 0 or event_counts.get("MULTIPLE_FACES", 0) > 0:
        m_faces = event_counts.get("MULTIPLE_FACES_DETECTED", 0) + event_counts.get("MULTIPLE_FACES", 0)
        evidence_bullets.append(f"• Multiple faces detected on webcam: {m_faces} event(s).")
    if event_counts.get("NO_FACE_DETECTED", 0) > 0 or event_counts.get("NO_FACE", 0) > 0:
        no_faces = event_counts.get("NO_FACE_DETECTED", 0) + event_counts.get("NO_FACE", 0)
        evidence_bullets.append(f"• Face absence detected on camera: {no_faces} event(s).")
    if event_counts.get("CONTINUOUS_VOICE_ACTIVITY", 0) > 0:
        evidence_bullets.append(f"• Continuous voice activity when interview silent: {event_counts['CONTINUOUS_VOICE_ACTIVITY']} event(s).")
    if event_counts.get("HIGH_AUDIO_SPIKE", 0) > 0 or event_counts.get("ADDITIONAL_VOICE", 0) > 0:
        spikes = event_counts.get("HIGH_AUDIO_SPIKE", 0) + event_counts.get("ADDITIONAL_VOICE", 0)
        evidence_bullets.append(f"• Audio spikes / secondary voice signals: {spikes} event(s).")
    if event_counts.get("MIC_MUTED_OR_DISCONNECTED", 0) > 0:
        evidence_bullets.append(f"• Microphone muted or disconnected: {event_counts['MIC_MUTED_OR_DISCONNECTED']} event(s).")

    # Compute Sub-Scores (Starting from 100.0)
    browser_score = max(0.0, 100.0 - category_penalties["browser"])
    webcam_score = max(0.0, 100.0 - category_penalties["webcam"])
    audio_score = max(0.0, 100.0 - category_penalties["audio"])
    code_similarity_score = 100.0  # Not applicable for live interview
    behavior_score = round((browser_score + webcam_score) / 2.0, 1)

    # Weighted Overall Integrity Score for Video Interview
    overall_integrity = round(
        (browser_score * 0.35) +
        (webcam_score * 0.35) +
        (audio_score * 0.30),
        1
    )

    # Determine Risk Level Category
    if overall_integrity >= 85.0:
        risk_level = RiskLevel.low_risk
    elif overall_integrity >= 60.0:
        risk_level = RiskLevel.review_recommended
    else:
        risk_level = RiskLevel.high_risk

    # Format AI-Assisted Integrity Summary
    summary_header = (
        f"AI-Assisted Video Interview Integrity Summary\n"
        f"Overall Integrity Score: {overall_integrity}%\n"
        f"Risk Level: {risk_level.value}\n\n"
        f"Observed Signals:\n"
    )
    if not evidence_bullets:
        evidence_bullets.append("• No suspicious activity or proctoring warnings recorded during interview.")

    summary_footer = (
        "\n\nImportant: These signals indicate potential proctoring flags. "
        "They do not automatically determine interview outcomes or disqualify candidates. "
        "Recruiter review is recommended."
    )
    ai_summary_text = summary_header + "\n".join(evidence_bullets) + summary_footer

    result_obj = db.query(IntegrityResult).filter(IntegrityResult.interview_id == interview.id).first()
    if not result_obj:
        result_obj = IntegrityResult(
            interview_id=interview.id,
            browser_score=browser_score,
            webcam_score=webcam_score,
            audio_score=audio_score,
            code_similarity_score=code_similarity_score,
            behavior_score=behavior_score,
            overall_integrity_score=overall_integrity,
            risk_level=risk_level,
            ai_summary=ai_summary_text,
        )
        db.add(result_obj)
    else:
        result_obj.browser_score = browser_score
        result_obj.webcam_score = webcam_score
        result_obj.audio_score = audio_score
        result_obj.code_similarity_score = code_similarity_score
        result_obj.behavior_score = behavior_score
        result_obj.overall_integrity_score = overall_integrity
        result_obj.risk_level = risk_level
        result_obj.ai_summary = ai_summary_text

    db.commit()
    db.refresh(result_obj)
    return result_obj

