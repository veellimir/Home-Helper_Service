from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.models import BaseORM


class SQLAlchemyBaseDAO[T: BaseORM]:
    def __init__(self, model: type[T]) -> None:
        self.model = model

    async def get_count_works(
        self,
        session: AsyncSession,
    ) -> int:
        stmt = select(func.count()).select_from(self.model)
        result = await session.execute(stmt)
        return result.scalar_one()

    async def get_list_objects_with_filters(
        self, session: AsyncSession, limit: int, cursor: int | None = None
    ) -> (list)[T]:
        stmt = select(self.model).order_by(self.model.id).limit(limit + 1)
        if cursor is not None:
            stmt = stmt.where(self.model.id > cursor)

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_object_by_id(
        self, session: AsyncSession, obj_id: int
    ) -> T | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
