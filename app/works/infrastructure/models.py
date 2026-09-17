from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.users.infrastructure.models import QuestionnaireORM
from core.infrastructure.models import BaseORM
from core.infrastructure.typing import INPUT_USER_DATE


class WorksORM(BaseORM):
    __tablename__ = "works"

    title: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    working_hour: Mapped[int] = mapped_column(Integer, nullable=False)

    bookings: Mapped[list["WorkBookingsORM"]] = relationship(
        back_populates="work"
    )


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

    questionnaire: Mapped["QuestionnaireORM"] = relationship(
        back_populates="work_bookings"
    )
    work: Mapped["WorksORM"] = relationship(back_populates="bookings")
