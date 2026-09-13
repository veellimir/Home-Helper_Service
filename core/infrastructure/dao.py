from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.models import BaseORM


class SQLAlchemyBaseDAO[T: BaseORM]:
    def __init__(self, model: type[T]) -> None:
        self.model = model

    async def get_list_objects(self, session: AsyncSession) -> list[T]:
        stmt = select(self.model)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_object_by_id(
        self, session: AsyncSession, obj_id: int
    ) -> T | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
