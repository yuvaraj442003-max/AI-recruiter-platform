"""create coding assessment module tables

Revision ID: 0007_create_coding_tables
Revises: cc283912283e
Create Date: 2026-09-09 18:50:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.core.db_types import GUID

# revision identifiers, used by Alembic.
revision: str = '0007_create_coding_tables'
down_revision: Union[str, None] = 'cc283912283e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create coding_questions table
    op.create_table(
        'coding_questions',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('difficulty', sa.String(length=50), nullable=False, server_default='Medium'),
        sa.Column('category', sa.String(length=100), nullable=False, server_default='Algorithms'),
        sa.Column('programming_languages', sa.Text(), nullable=True),
        sa.Column('starter_code', sa.Text(), nullable=True),
        sa.Column('expected_output', sa.Text(), nullable=True),
        sa.Column('constraints', sa.Text(), nullable=True),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # Create coding_test_cases table
    op.create_table(
        'coding_test_cases',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('question_id', GUID(), sa.ForeignKey('coding_questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('input_data', sa.Text(), nullable=False),
        sa.Column('expected_output', sa.Text(), nullable=False),
        sa.Column('is_hidden', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('points', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # Create coding_assessments table
    op.create_table(
        'coding_assessments',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('job_id', GUID(), sa.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('passing_score', sa.Float(), nullable=False, server_default='60.0'),
        sa.Column('total_score', sa.Float(), nullable=False, server_default='100.0'),
        sa.Column('max_attempts', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('allowed_languages', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # Create coding_assessment_questions table
    op.create_table(
        'coding_assessment_questions',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('assessment_id', GUID(), sa.ForeignKey('coding_assessments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', GUID(), sa.ForeignKey('coding_questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_order', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('points', sa.Float(), nullable=False, server_default='20.0')
    )

    # Create candidate_coding_attempts table
    op.create_table(
        'candidate_coding_attempts',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('candidate_id', GUID(), sa.ForeignKey('candidate_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessment_id', GUID(), sa.ForeignKey('coding_assessments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='Not Started'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('percentage', sa.Float(), nullable=True),
        sa.Column('passed', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('time_taken', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # Create coding_submissions table
    op.create_table(
        'coding_submissions',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('attempt_id', GUID(), sa.ForeignKey('candidate_coding_attempts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', GUID(), sa.ForeignKey('coding_questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('language', sa.String(length=50), nullable=False),
        sa.Column('source_code', sa.Text(), nullable=False),
        sa.Column('execution_status', sa.String(length=50), nullable=False, server_default='Success'),
        sa.Column('test_cases_passed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('test_cases_total', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('functional_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('quality_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('efficiency_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('complexity_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('time_complexity', sa.String(length=50), nullable=True),
        sa.Column('space_complexity', sa.String(length=50), nullable=True),
        sa.Column('ai_review', sa.Text(), nullable=True),
        sa.Column('execution_time', sa.Float(), nullable=True),
        sa.Column('memory_used', sa.Float(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # Add columns to applications table
    try:
        op.add_column('applications', sa.Column('coding_score', sa.Float(), nullable=True))
        op.add_column('applications', sa.Column('interview_score', sa.Float(), nullable=True))
        op.add_column('applications', sa.Column('overall_score', sa.Float(), nullable=True))
    except Exception:
        pass


def downgrade() -> None:
    op.drop_column('applications', 'overall_score')
    op.drop_column('applications', 'interview_score')
    op.drop_column('applications', 'coding_score')
    op.drop_table('coding_submissions')
    op.drop_table('candidate_coding_attempts')
    op.drop_table('coding_assessment_questions')
    op.drop_table('coding_assessments')
    op.drop_table('coding_test_cases')
    op.drop_table('coding_questions')
