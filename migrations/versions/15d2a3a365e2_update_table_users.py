"""Update table users

Revision ID: 15d2a3a365e2
Revises: ffacb55f5848
Create Date: 2026-09-13 20:22:29.748324

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "15d2a3a365e2"
down_revision: str | Sequence[str] | None = "ffacb55f5848"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("email", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=False),
    )
    op.alter_column(
        "users",
        "username",
        existing_type=sa.VARCHAR(length=20),
        nullable=True,
    )
    op.create_unique_constraint(None, "users", ["email"])
    op.drop_column("users", "password")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "password",
            sa.VARCHAR(length=15),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(None, "users", type_="unique")
    op.alter_column(
        "users",
        "username",
        existing_type=sa.VARCHAR(length=20),
        nullable=False,
    )
    op.drop_column("users", "password_hash")
    op.drop_column("users", "email")
