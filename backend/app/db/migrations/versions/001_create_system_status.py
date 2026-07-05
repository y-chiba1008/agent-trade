"""create system_status

Revision ID: 001_create_system_status
Revises:
Create Date: 2026-07-04

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '001_create_system_status'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'system_status',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('last_heartbeat_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('system_status')
