"""reate table associations user lessons

Revision ID: c8b639d88f5b
Revises: 1ed6e112c0ed
Create Date: 2026-09-11 21:33:24.663089

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c8b639d88f5b"
down_revision: str | Sequence[str] | None = "1ed6e112c0ed"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lessons",
        sa.Column("title", sa.String(length=30), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=False),
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
    )
    op.create_table(
        "user_lessons",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lesson_id", sa.Integer(), nullable=False),
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
            ["lesson_id"], ["lessons.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "lesson_id", name="uq_user_lessons_user_lesson"
        ),
    )


def downgrade() -> None:
    op.drop_table("user_lessons")
    op.drop_table("lessons")
