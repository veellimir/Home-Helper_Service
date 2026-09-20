"""create password reset tokens

Revision ID: 22eb0502d3ac
Revises: 76fa8a18b6b6
Create Date: 2026-09-20 10:20:56.761054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '22eb0502d3ac'
down_revision: Union[str, Sequence[str], None] = '76fa8a18b6b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('password_reset_tokens',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token_hash', sa.String(length=64), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('used_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token_hash')
    )


def downgrade() -> None:
    op.drop_table('password_reset_tokens')
