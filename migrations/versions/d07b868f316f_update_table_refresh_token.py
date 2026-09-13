"""Update table refresh token

Revision ID: d07b868f316f
Revises: 15d2a3a365e2
Create Date: 2026-09-13 20:41:50.278860

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d07b868f316f"
down_revision: str | Sequence[str] | None = "15d2a3a365e2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoker_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', 'now')"),
            nullable=False,
        ),
        sa.Column(
            "update_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', 'now')"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index(
        op.f("ix_refresh_tokens_user_id"),
        "refresh_tokens",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_refresh_tokens_user_id"), table_name="refresh_tokens"
    )
    op.drop_table("refresh_tokens")
