"""
Job recommendation endpoint — ranks all published jobs against the
current candidate's profile and returns the top matches.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.job import JobResponse
from app.services.job_service import recommend_jobs_for_candidate

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/jobs", response_model=APIResponse[list[dict]])
def get_recommended_jobs(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    scored = recommend_jobs_for_candidate(db, current_user.id, limit=limit)
    data = [
        {
            "job": JobResponse.from_job(item["job"]).model_dump(mode="json"),
            "match_score": item["match_score"],
            "breakdown": item["breakdown"],
        }
        for item in scored
    ]
    return APIResponse(success=True, message="Recommended jobs", data=data)


@router.get("/campus-jobs", response_model=APIResponse[list[dict]])
def get_campus_recommended_jobs(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    """
    Ranks published jobs and internships for college students, providing skill-gap
    analysis and linking missing skills directly to platform study materials.
    """
    from app.models.candidate import CandidateProfile
    from app.models.student import StudyMaterial
    from app.ml.ranking import compute_match

    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    scored = recommend_jobs_for_candidate(db, current_user.id, limit=limit)

    all_materials = db.query(StudyMaterial).all()

    cand_skills = {cs.skill.skill_name.lower() for cs in profile.candidate_skills if cs.skill} if profile else set()

    campus_data = []
    for item in scored:
        job = item["job"]
        req_skills = [js.skill.skill_name for js in job.job_skills if js.skill and js.required]
        pref_skills = [js.skill.skill_name for js in job.job_skills if js.skill and not js.required]
        matched_req = [s for s in req_skills if s.lower() in cand_skills]
        all_missing = [s for s in req_skills + pref_skills if s.lower() not in cand_skills]

        # Map missing skills to relevant study materials (via Qdrant semantic search with fallback)
        suggested_prep = []
        for skill in all_missing[:4]:
            matched_via_qdrant = False
            try:
                from app.services.qdrant_service import search as vector_search, COLLECTION_LEARNING
                q_res = vector_search(COLLECTION_LEARNING, query_text=skill, limit=1)
                if q_res:
                    res_p = q_res[0].get("payload", {})
                    if res_p.get("title"):
                        suggested_prep.append({
                            "skill": skill,
                            "material_title": res_p["title"],
                            "material_slug": res_p.get("slug", "campus-placement-60-day-sprint"),
                            "category": res_p.get("category", "core_cs"),
                        })
                        matched_via_qdrant = True
            except Exception:
                pass

            if not matched_via_qdrant:
                matched_mat = next(
                    (m for m in all_materials if skill.lower() in m.title.lower() or (m.tags_json and skill.lower() in m.tags_json.lower())),
                    None
                )
                if matched_mat:
                    suggested_prep.append({
                        "skill": skill,
                        "material_title": matched_mat.title,
                        "material_slug": matched_mat.slug,
                        "category": matched_mat.category,
                    })
                else:
                    suggested_prep.append({
                        "skill": skill,
                        "material_title": "Campus Placement 60-Day Master Sprint Guide",
                        "material_slug": "campus-placement-60-day-sprint",
                        "category": "interview_prep",
                    })

        job_dict = JobResponse.from_job(job).model_dump(mode="json")
        is_fresher_suitable = (job.experience_required is None or job.experience_required <= 1.0)

        campus_data.append({
            "job": job_dict,
            "match_score": item["match_score"],
            "breakdown": item["breakdown"],
            "matched_skills": matched_req,
            "missing_skills": all_missing,
            "suggested_prep": suggested_prep,
            "is_fresher_friendly": is_fresher_suitable,
            "campus_tier": "Elite Campus Drive" if item["match_score"] >= 80 else "Recommended Placement Opportunity",
        })

    return APIResponse(success=True, message="Campus placement recommendations with skill gap analysis", data=campus_data)

