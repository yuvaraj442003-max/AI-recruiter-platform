"""create candidate profile, skills, candidate_skills tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-18

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from app.core.db_types import GUID

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "candidate_profiles",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("user_id", GUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("experience_years", sa.Float(), nullable=True),
        sa.Column("education", sa.Text(), nullable=True),
        sa.Column("resume_path", sa.String(length=500), nullable=True),
        sa.Column("resume_text", sa.Text(), nullable=True),
        sa.Column("resume_original_filename", sa.String(length=255), nullable=True),
        sa.Column("profile_score", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "skills",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("skill_name", sa.String(length=150), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
    )
    op.create_index("ix_skills_skill_name", "skills", ["skill_name"], unique=True)

    op.create_table(
        "candidate_skills",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("candidate_id", GUID(), sa.ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill_id", GUID(), sa.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False),
        sa.Column("proficiency", sa.String(length=50), nullable=True),
        sa.Column("years_of_experience", sa.Float(), nullable=True),
        sa.UniqueConstraint("candidate_id", "skill_id", name="uq_candidate_skill"),
    )


def downgrade() -> None:
    op.drop_table("candidate_skills")
    op.drop_index("ix_skills_skill_name", table_name="skills")
    op.drop_table("skills")
    op.drop_table("candidate_profiles")
