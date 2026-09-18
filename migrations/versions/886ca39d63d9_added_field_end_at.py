"""added field end_at

Revision ID: 886ca39d63d9
Revises: 9ddd8434415c
Create Date: 2026-09-18 17:08:59.693131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '886ca39d63d9'
down_revision: Union[str, Sequence[str], None] = '9ddd8434415c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('work_bookings', sa.Column('end_at', sa.DateTime(), nullable=False))


def downgrade() -> None:
    op.drop_column('work_bookings', 'end_at')
