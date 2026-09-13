from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.infrastructure.models import BaseORM


class WorksORM(BaseORM):
    __tablename__ = "works"

    title: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    working_hour: Mapped[int] = mapped_column(Integer, nullable=False)
