"""create interview tables

Revision ID: 0005
Revises: 0004
Create Date: 2026-08-18

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from app.core.db_types import GUID

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "interviews",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("candidate_id", GUID(), sa.ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", GUID(), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("application_id", GUID(), sa.ForeignKey("applications.id", ondelete="SET NULL"), nullable=True),
        sa.Column(
            "interview_type",
            sa.Enum("technical", "behavioral", "mixed", "ai_interview", name="interview_type"),
            nullable=False,
            server_default="mixed",
        ),
        sa.Column(
            "status",
            sa.Enum("scheduled", "in_progress", "completed", name="interview_status"),
            nullable=False,
            server_default="scheduled",
        ),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "interview_questions",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("interview_id", GUID(), sa.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("question_type", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.Text(), nullable=False),
        sa.Column("expected_topics", sa.Text(), nullable=True),
        sa.Column("order_number", sa.Integer(), nullable=False),
    )

    op.create_table(
        "interview_answers",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("question_id", GUID(), sa.ForeignKey("interview_questions.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("candidate_id", GUID(), sa.ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("answer_source", sa.Text(), nullable=False, server_default="text"),
        sa.Column("answer_score", sa.Float(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "interview_evaluations",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("interview_id", GUID(), sa.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("technical_score", sa.Float(), nullable=True),
        sa.Column("communication_score", sa.Float(), nullable=True),
        sa.Column("relevance_score", sa.Float(), nullable=True),
        sa.Column("problem_solving_score", sa.Float(), nullable=True),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("strengths", sa.Text(), nullable=True),
        sa.Column("weaknesses", sa.Text(), nullable=True),
        sa.Column("recommendation", sa.Text(), nullable=True),
        sa.Column("source", sa.Text(), nullable=False, server_default="template"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("interview_evaluations")
    op.drop_table("interview_answers")
    op.drop_table("interview_questions")
    op.drop_table("interviews")
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("DROP TYPE IF EXISTS interview_type")
        op.execute("DROP TYPE IF EXISTS interview_status")
