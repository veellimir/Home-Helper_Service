from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.works.domain.exceptions import WorkNotFoundException
from app.works.infrastructure.dao import WorksDAO
from app.works.infrastructure.models import WorksORM
from app.works.infrastructure.schemes import (
    CreateWorkSchem,
    UpdateWorkSchem,
    WorkResponseSchem,
    WorksListResponseSchem,
)
from core.domain.service import SQLAlchemyBaseService


class WorksService(SQLAlchemyBaseService[WorksORM]):
    def __init__(self, dao: WorksDAO) -> None:
        self.dao = dao
        super().__init__(self.dao)

    async def get_list_works(
        self, session: AsyncSession
    ) -> list[WorksListResponseSchem]:
        works: list[WorksORM] = await self.dao.get_list_objects(
            session=session
        )
        return [WorksListResponseSchem.model_validate(work) for work in works]

    async def get_work_by_id(
        self, session: AsyncSession, work_id: int
    ) -> WorkResponseSchem | None:
        current_work: WorksORM | None = await self.dao.get_object_by_id(
            session=session, obj_id=work_id
        )
        if not current_work:
            raise WorkNotFoundException

        return WorkResponseSchem.model_validate(current_work)

    async def create_work(
        self,
        session: AsyncSession,
        data_work: CreateWorkSchem,
    ) -> WorkResponseSchem:
        new_work: WorksORM = await self.dao.create_work(
            session=session, data_work=data_work
        )
        return WorkResponseSchem.model_validate(new_work)

    async def patch_work_by_id(
        self,
        session: AsyncSession,
        work_id: int,
        data_work: UpdateWorkSchem,
    ) -> WorkResponseSchem | None:
        current_work: WorksORM | None = await self.dao.get_object_by_id(
            session=session, obj_id=work_id
        )
        if not current_work:
            raise WorkNotFoundException

        update_work: dict[str, Any] = {
            "title": data_work.title,
            "description": data_work.description,
            "start_date": data_work.start_date,
            "end_date": data_work.end_date,
        }

        result: WorksORM = await self.dao.patch_work_by_id(
            session=session, work=current_work, data_lesson=update_work
        )
        return WorkResponseSchem.model_validate(result)

    async def delete_work_by_id(
        self,
        session: AsyncSession,
        work_id: int,
    ) -> None:
        pass
