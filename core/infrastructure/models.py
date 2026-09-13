from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
)

from core.infrastructure.typing import CREATED_AT, INT_PK, UPDATE_AT


class BaseORM(DeclarativeBase):
    id: Mapped[INT_PK]
    created_at: Mapped[CREATED_AT]
    update_at: Mapped[UPDATE_AT]
