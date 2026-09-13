from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.users.domain.enums import UserRole
from core.infrastructure.models import BaseORM


class UsersORM(BaseORM):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "username IS NOT NULL OR email IS NOT NULL",
            name="ck_users_username_or_email",
        ),
    )

    username: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=True
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String(25), default=UserRole.USER)

    questionnaire: Mapped["QuestionnaireORM | None"] = relationship(
        back_populates="user",
        uselist=False,
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
