"""added field image_url

Revision ID: 917f12f655bc
Revises: 886ca39d63d9
Create Date: 2026-09-18 21:22:30.381423

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "917f12f655bc"
down_revision: str | Sequence[str] | None = "886ca39d63d9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "works", sa.Column("image_url", sa.String(length=500), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("works", "image_url")
