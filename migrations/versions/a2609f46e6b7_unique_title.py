"""unique title

Revision ID: a2609f46e6b7
Revises: c8b639d88f5b
Create Date: 2026-09-12 14:41:55.243519

"""

from collections.abc import Sequence

from alembic import op

revision: str = "a2609f46e6b7"
down_revision: str | Sequence[str] | None = "c8b639d88f5b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(None, "lessons", ["title"])


def downgrade() -> None:
    op.drop_constraint(None, "lessons", type_="unique")
