from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.works.infrastructure.models import WorksORM
from app.works.infrastructure.schemes import CreateWorkSchem
from core.infrastructure.dao import SQLAlchemyBaseDAO


class WorksDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = WorksORM
        super().__init__(WorksORM)

    async def get_work_by_title(
        self, session: AsyncSession, title: str
    ) -> WorksORM | None:
        stmt = select(self.model).where(self.model.title == title)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_work(
        self,
        session: AsyncSession,
        data_work: CreateWorkSchem,
        image_url: str | None = None,
    ) -> WorksORM:
        new_work = self.model(
            title=data_work.title,
            description=data_work.description,
            price=data_work.price,
            working_hour=data_work.working_hour,
            image_url=image_url,
        )

        session.add(new_work)
        await session.flush()

        return new_work

    async def patch_work_by_id(
        self,
        session: AsyncSession,
        work: WorksORM,
        data_work: dict[str, Any],
    ) -> WorksORM:
        for field, value in data_work.items():
            setattr(work, field, value)

        await session.flush()
        return work

    async def delete_work(
        self, session: AsyncSession, current_work: WorksORM
    ) -> None:
        await session.delete(current_work)
        await session.flush()
