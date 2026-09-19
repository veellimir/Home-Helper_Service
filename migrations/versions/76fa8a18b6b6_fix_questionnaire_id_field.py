"""fix questionnaire_id field

Revision ID: 76fa8a18b6b6
Revises: 917f12f655bc
Create Date: 2026-09-19 09:43:13.643000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "76fa8a18b6b6"
down_revision: str | Sequence[str] | None = "917f12f655bc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        op.f("work_bookings_questionnaire_id_key"), "work_bookings"
    )
    op.drop_constraint(op.f("work_bookings_work_id_key"), "work_bookings")


def downgrade() -> None:
    op.create_unique_constraint(
        op.f("work_bookings_work_id_key"),
        "work_bookings",
        ["work_id"],
        postgresql_nulls_not_distinct=False,
    )
    op.create_unique_constraint(
        op.f("work_bookings_questionnaire_id_key"),
        "work_bookings",
        ["questionnaire_id"],
        postgresql_nulls_not_distinct=False,
    )
