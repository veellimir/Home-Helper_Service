from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.users.domain.enums import UserRoleEnum
from core.infrastructure.models import BaseORM

if TYPE_CHECKING:
    from app.works.infrastructure.models import WorkBookingsORM


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
    role: Mapped[str] = mapped_column(String(25), default=UserRoleEnum.CLIENT)

    refresh_tokens: Mapped[list["RefreshTokenORM"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    questionnaire: Mapped["QuestionnaireORM | None"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class RefreshTokenORM(BaseORM):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoker_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["UsersORM"] = relationship(back_populates="refresh_tokens")


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
    work_bookings: Mapped[list["WorkBookingsORM"]] = relationship(
        back_populates="questionnaire",
        cascade="all, delete-orphan",
    )
