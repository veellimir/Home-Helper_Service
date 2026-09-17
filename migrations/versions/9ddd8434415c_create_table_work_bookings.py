"""create table work_bookings

Revision ID: 9ddd8434415c
Revises: d07b868f316f
Create Date: 2026-09-17 21:56:15.911604

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9ddd8434415c"
down_revision: str | Sequence[str] | None = "d07b868f316f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "work_bookings",
        sa.Column("questionnaire_id", sa.Integer(), nullable=False),
        sa.Column("work_id", sa.Integer(), nullable=False),
        sa.Column("start_at", sa.DateTime(), nullable=False),
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
            ["questionnaire_id"], ["questionnaires.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["work_id"], ["works.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("questionnaire_id"),
        sa.UniqueConstraint("work_id"),
    )


def downgrade() -> None:
    op.drop_table("work_bookings")
