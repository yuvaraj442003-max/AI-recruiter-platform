"""ai_aptitude_generator_tables

Revision ID: ee45b91a23c1
Revises: cc283912283e
Create Date: 2026-10-15 16:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ee45b91a23c1'
down_revision: Union[str, Sequence[str], None] = ('cc283912283e', '0009_proctoring_system_upgrade')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Update aptitude_tests
    op.add_column('aptitude_tests', sa.Column('topics_json', sa.Text(), nullable=True))
    op.add_column('aptitude_tests', sa.Column('difficulty', sa.String(length=50), server_default='mixed', nullable=False))
    op.add_column('aptitude_tests', sa.Column('marks_per_question', sa.Float(), server_default='1.0', nullable=False))
    op.add_column('aptitude_tests', sa.Column('total_marks', sa.Float(), server_default='15.0', nullable=False))
    op.add_column('aptitude_tests', sa.Column('status', sa.String(length=50), server_default='published', nullable=False))
    op.add_column('aptitude_tests', sa.Column('created_by_user_id', sa.UUID(), nullable=True))

    # 2. Update aptitude_questions
    op.add_column('aptitude_questions', sa.Column('test_id', sa.UUID(), nullable=True))
    op.add_column('aptitude_questions', sa.Column('topic_name', sa.String(length=150), nullable=True))
    op.add_column('aptitude_questions', sa.Column('marks', sa.Float(), server_default='1.0', nullable=False))

    # 3. Create aptitude_options
    op.create_table(
        'aptitude_options',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('question_id', sa.UUID(), sa.ForeignKey('aptitude_questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('option_letter', sa.String(length=5), nullable=False),
        sa.Column('option_text', sa.Text(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('order_index', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_aptitude_options_question_id', 'aptitude_options', ['question_id'])

    # 4. Create candidate_test_attempts
    op.create_table(
        'candidate_test_attempts',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('test_id', sa.UUID(), sa.ForeignKey('aptitude_tests.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='In Progress', nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('total_marks', sa.Float(), nullable=True),
        sa.Column('percentage', sa.Float(), nullable=True),
        sa.Column('passed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('time_taken_seconds', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_candidate_test_attempts_user_id', 'candidate_test_attempts', ['user_id'])
    op.create_index('ix_candidate_test_attempts_test_id', 'candidate_test_attempts', ['test_id'])

    # 5. Create candidate_answers
    op.create_table(
        'candidate_answers',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('attempt_id', sa.UUID(), sa.ForeignKey('candidate_test_attempts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', sa.UUID(), sa.ForeignKey('aptitude_questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('selected_option_id', sa.UUID(), sa.ForeignKey('aptitude_options.id', ondelete='SET NULL'), nullable=True),
        sa.Column('selected_option_index', sa.Integer(), nullable=True),
        sa.Column('selected_option_letter', sa.String(length=5), nullable=True),
        sa.Column('is_correct', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('marks_awarded', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_candidate_answers_attempt_id', 'candidate_answers', ['attempt_id'])
    op.create_index('ix_candidate_answers_question_id', 'candidate_answers', ['question_id'])

    # 6. Create aptitude_test_results
    op.create_table(
        'aptitude_test_results',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('attempt_id', sa.UUID(), sa.ForeignKey('candidate_test_attempts.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('test_id', sa.UUID(), sa.ForeignKey('aptitude_tests.id', ondelete='CASCADE'), nullable=False),
        sa.Column('candidate_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_questions', sa.Integer(), server_default='0', nullable=False),
        sa.Column('correct_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('wrong_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('unanswered_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('score', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('total_marks', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('percentage', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('passed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('percentile_estimate', sa.Float(), server_default='50.0', nullable=False),
        sa.Column('topic_breakdown_json', sa.Text(), nullable=True),
        sa.Column('feedback_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_aptitude_test_results_test_id', 'aptitude_test_results', ['test_id'])
    op.create_index('ix_aptitude_test_results_candidate_id', 'aptitude_test_results', ['candidate_id'])


def downgrade() -> None:
    op.drop_table('aptitude_test_results')
    op.drop_table('candidate_answers')
    op.drop_table('candidate_test_attempts')
    op.drop_table('aptitude_options')
    op.drop_column('aptitude_questions', 'marks')
    op.drop_column('aptitude_questions', 'topic_name')
    op.drop_column('aptitude_questions', 'test_id')
    op.drop_column('aptitude_tests', 'created_by_user_id')
    op.drop_column('aptitude_tests', 'status')
    op.drop_column('aptitude_tests', 'total_marks')
    op.drop_column('aptitude_tests', 'marks_per_question')
    op.drop_column('aptitude_tests', 'difficulty')
    op.drop_column('aptitude_tests', 'topics_json')
