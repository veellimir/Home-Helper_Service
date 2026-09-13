"""Create table users, questionnaires

Revision ID: 1ed6e112c0ed
Revises:
Create Date: 2026-09-08 20:51:36.036547

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "1ed6e112c0ed"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("password", sa.String(length=15), nullable=False),
        sa.Column("role", sa.String(length=25), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "questionnaires",
        sa.Column(
            "first_name",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "last_name",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
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
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("questionnaires")
    op.drop_table("users")
