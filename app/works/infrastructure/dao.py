from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.works.infrastructure.models import WorksORM
from app.works.infrastructure.schemes import CreateWorkSchem
from core.infrastructure.dao import SQLAlchemyBaseDAO


class WorksDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = WorksORM
        super().__init__(WorksORM)

    async def create_work(
        self,
        session: AsyncSession,
        data_work: CreateWorkSchem,
    ) -> WorksORM:
        new_work = self.model(
            title=data_work.title,
            description=data_work.description,
            start_date=data_work.start_date,
            end_date=data_work.end_date,
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
