"""create email settings, calendar connection, and scheduled interview tables

Revision ID: 0008_email_calendar_system
Revises: 0007_create_coding_tables
Create Date: 2026-09-09 21:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.core.db_types import GUID

revision: str = '0008_email_calendar_system'
down_revision: Union[str, None] = '0007_create_coding_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create calendar_connections table
    op.create_table(
        'calendar_connections',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('recruiter_id', GUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('access_token_encrypted', sa.Text(), nullable=True),
        sa.Column('refresh_token_encrypted', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('connected', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('account_email', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # 2. Create scheduled_interviews table
    op.create_table(
        'scheduled_interviews',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('interview_id', GUID(), sa.ForeignKey('interviews.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('candidate_id', GUID(), sa.ForeignKey('candidate_profiles.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('recruiter_id', GUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('job_id', GUID(), sa.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('interview_type', sa.String(length=100), nullable=False, server_default='AI Technical Interview'),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('start_time_utc', sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column('end_time_utc', sa.DateTime(timezone=True), nullable=False),
        sa.Column('timezone', sa.String(length=100), nullable=False, server_default='UTC'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='SCHEDULED', index=True),
        sa.Column('calendar_provider', sa.String(length=50), nullable=True),
        sa.Column('calendar_event_id', sa.String(length=255), nullable=True),
        sa.Column('calendar_event_url', sa.Text(), nullable=True),
        sa.Column('calendar_sync_status', sa.String(length=50), nullable=False, server_default='synced'),
        sa.Column('reminder_24h_sent', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('reminder_1h_sent', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('cancelled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # 3. Create recruiter_email_settings table
    op.create_table(
        'recruiter_email_settings',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('recruiter_id', GUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True),
        sa.Column('app_received', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('candidate_shortlisted', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('interview_invited', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('interview_reminder', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('interview_rescheduled', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('interview_cancelled', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('candidate_rejected', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    )


def downgrade() -> None:
    op.drop_table('recruiter_email_settings')
    op.drop_table('scheduled_interviews')
    op.drop_table('calendar_connections')
