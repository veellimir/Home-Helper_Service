"""added status, comment

Revision ID: dd410dd92161
Revises: cd33eed89cae
Create Date: 2026-09-26 19:55:12.351166

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "dd410dd92161"
down_revision: str | Sequence[str] | None = "cd33eed89cae"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "work_bookings",
        sa.Column(
            "status",
            sa.Enum(
                "WAITING",
                "ACCEPTED",
                "EDITING",
                "CANCELLED",
                name="statusbookingenum",
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "work_bookings",
        sa.Column("comment", sa.String(length=256), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("work_bookings", "comment")
    op.drop_column("work_bookings", "status")
