from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.infrastructure.models import BaseORM

if TYPE_CHECKING:
    from app.lessons.infrastructure.models import LessonsORM
    from app.users.infrastructure.models import UsersORM


class UserLessonORM(BaseORM):
    """Связывает занятия - пользователи"""

    __tablename__ = "user_lessons"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "lesson_id",
            name="uq_user_lessons_user_lesson",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["UsersORM"] = relationship(back_populates="user_lessons")
    lesson: Mapped["LessonsORM"] = relationship(back_populates="user_lessons")
