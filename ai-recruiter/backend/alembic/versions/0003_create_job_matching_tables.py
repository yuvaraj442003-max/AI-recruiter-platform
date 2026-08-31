"""create jobs, job_skills, applications tables

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-18

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from app.core.db_types import GUID

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("recruiter_id", GUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column(
            "employment_type",
            sa.Enum("full_time", "part_time", "contract", "internship", name="employment_type"),
            nullable=False,
            server_default="full_time",
        ),
        sa.Column("experience_required", sa.Float(), nullable=True),
        sa.Column("salary_range", sa.String(length=100), nullable=True),
        sa.Column(
            "status",
            sa.Enum("draft", "published", "closed", name="job_status"),
            nullable=False,
            server_default="published",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "job_skills",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("job_id", GUID(), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_id", GUID(), sa.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),
    )

    op.create_table(
        "applications",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("candidate_id", GUID(), sa.ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", GUID(), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "applied", "under_review", "shortlisted", "interview", "selected", "rejected",
                name="application_status",
            ),
            nullable=False,
            server_default="applied",
        ),
        sa.Column("match_score", sa.Float(), nullable=True),
        sa.Column("match_breakdown", sa.Text(), nullable=True),
        sa.Column("applied_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("candidate_id", "job_id", name="uq_candidate_job_application"),
    )


def downgrade() -> None:
    op.drop_table("applications")
    op.drop_table("job_skills")
    op.drop_table("jobs")
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("DROP TYPE IF EXISTS application_status")
        op.execute("DROP TYPE IF EXISTS employment_type")
        op.execute("DROP TYPE IF EXISTS job_status")
