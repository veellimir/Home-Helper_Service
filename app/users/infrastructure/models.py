from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.lessons.infrastructure.models import UserLessonORM
from core.infrastructure.models import BaseORM


class UsersORM(BaseORM):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(15))
    role: Mapped[str] = mapped_column(String(25))

    questionnaire: Mapped["QuestionnaireORM | None"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    user_lessons: Mapped[list["UserLessonORM"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class QuestionnaireORM(BaseORM):
    __tablename__ = "questionnaires"

    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int | None] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    user: Mapped["UsersORM"] = relationship(
        back_populates="questionnaire",
    )
