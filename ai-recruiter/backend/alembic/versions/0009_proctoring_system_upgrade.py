"""proctoring system upgrade for assessments and interviews

Revision ID: 0009_proctoring_system_upgrade
Revises: 0008_email_calendar_system
Create Date: 2026-09-23 15:40:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.core.db_types import GUID

revision: str = '0009_proctoring_system_upgrade'
down_revision: Union[str, None] = '0008_email_calendar_system'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Relax attempt_id nullability
    with op.batch_alter_table('assessment_events', schema=None) as batch_op:
        batch_op.alter_column('attempt_id', existing_type=GUID(), nullable=True)
        batch_op.add_column(sa.Column('interview_id', GUID(), sa.ForeignKey('interviews.id', ondelete='SET NULL'), nullable=True))
        batch_op.add_column(sa.Column('assessment_id', GUID(), sa.ForeignKey('coding_assessments.id', ondelete='SET NULL'), nullable=True))
        batch_op.add_column(sa.Column('duration_seconds', sa.Float(), nullable=True))

    with op.batch_alter_table('assessment_consents', schema=None) as batch_op:
        batch_op.alter_column('attempt_id', existing_type=GUID(), nullable=True)
        batch_op.add_column(sa.Column('interview_id', GUID(), sa.ForeignKey('interviews.id', ondelete='SET NULL'), nullable=True))

    with op.batch_alter_table('integrity_results', schema=None) as batch_op:
        batch_op.alter_column('attempt_id', existing_type=GUID(), nullable=True)
        batch_op.add_column(sa.Column('interview_id', GUID(), sa.ForeignKey('interviews.id', ondelete='SET NULL'), nullable=True))
        batch_op.add_column(sa.Column('assessment_id', GUID(), sa.ForeignKey('coding_assessments.id', ondelete='SET NULL'), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('integrity_results', schema=None) as batch_op:
        batch_op.drop_column('assessment_id')
        batch_op.drop_column('interview_id')
        batch_op.alter_column('attempt_id', existing_type=GUID(), nullable=False)

    with op.batch_alter_table('assessment_consents', schema=None) as batch_op:
        batch_op.drop_column('interview_id')
        batch_op.alter_column('attempt_id', existing_type=GUID(), nullable=False)

    with op.batch_alter_table('assessment_events', schema=None) as batch_op:
        batch_op.drop_column('duration_seconds')
        batch_op.drop_column('assessment_id')
        batch_op.drop_column('interview_id')
        batch_op.alter_column('attempt_id', existing_type=GUID(), nullable=False)
