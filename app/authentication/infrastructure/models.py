from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.infrastructure.models import BaseORM
from core.infrastructure.typing import CREATED_AT

if TYPE_CHECKING:
    from app.users.infrastructure.models import UsersORM


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


class PasswordResetTokenORM(BaseORM):
    __tablename__ = "password_reset_tokens"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )
    expires_at: Mapped[CREATED_AT] = mapped_column(
        DateTime,
        nullable=False
    )
    used_at: Mapped[CREATED_AT | None] = mapped_column(
        DateTime,
        nullable=False
    )