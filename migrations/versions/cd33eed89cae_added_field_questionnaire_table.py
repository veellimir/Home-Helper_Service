"""added field questionnaire table

Revision ID: cd33eed89cae
Revises: 0c13e1abb3e4
Create Date: 2026-09-24 21:43:33.246648

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "cd33eed89cae"
down_revision: str | Sequence[str] | None = "0c13e1abb3e4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "questionnaires",
        sa.Column("phone", sa.String(length=12), nullable=True),
    )
    op.add_column(
        "questionnaires",
        sa.Column("address", sa.String(length=256), nullable=True),
    )
    op.create_unique_constraint(None, "questionnaires", ["phone"])
    op.create_unique_constraint(None, "questionnaires", ["address"])


def downgrade() -> None:
    op.drop_constraint(None, "questionnaires", type_="unique")
    op.drop_constraint(None, "questionnaires", type_="unique")
    op.drop_column("questionnaires", "address")
    op.drop_column("questionnaires", "phone")
