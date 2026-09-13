from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.infrastructure.associations_models import UserLessonORM
from core.infrastructure.models import BaseORM
from core.infrastructure.typing import INPUT_USER_DATE


class LessonsORM(BaseORM):
    __tablename__ = "lessons"

    title: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(Text)
    start_date: Mapped[INPUT_USER_DATE]
    end_date: Mapped[INPUT_USER_DATE]

    user_lessons: Mapped[list["UserLessonORM"]] = relationship(
        back_populates="lesson",
        cascade="all, delete-orphan",
    )
