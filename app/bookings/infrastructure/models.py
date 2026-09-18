from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.users.infrastructure.models import QuestionnaireORM
from core.infrastructure.models import BaseORM
from core.infrastructure.typing import INPUT_USER_DATE

if TYPE_CHECKING:
    from app.works.infrastructure.models import WorksORM


class WorkBookingsORM(BaseORM):
    __tablename__ = "work_bookings"

    questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey("questionnaires.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    work_id: Mapped[int] = mapped_column(
        ForeignKey("works.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    start_at: Mapped[INPUT_USER_DATE]
    end_at: Mapped[INPUT_USER_DATE]

    questionnaire: Mapped["QuestionnaireORM"] = relationship(
        back_populates="work_bookings"
    )
    work: Mapped["WorksORM"] = relationship(back_populates="bookings")
