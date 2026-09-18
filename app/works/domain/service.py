from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.works.domain.exceptions import (
    WorkConflictException,
    WorkNotFoundException,
)
from app.works.infrastructure.dao import WorksDAO
from app.works.infrastructure.models import WorksORM
from app.works.infrastructure.schemes import (
    CreateWorkSchem,
    UpdateWorkSchem,
    WorkResponseSchem,
    WorksListResponseSchem,
)
from core.domain.service import SQLAlchemyBaseService


class Utils:
    @staticmethod
    def save_image_from_work(image: UploadFile) -> str:
        directory = Path("media/works_img")
        directory.mkdir(parents=True, exist_ok=True)

        extension = Path(image.filename or "").suffix.lower()
        filename = f"{uuid4()}{extension}"

        file_path = directory / filename

        content = image.read()
        file_path.write_bytes(content)

        return f"/media/works_img/{filename}"


class WorksService(SQLAlchemyBaseService[WorksORM]):
    def __init__(self, dao: WorksDAO) -> None:
        self.dao = dao
        self.utils = Utils()
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
        image: UploadFile | None,
    ) -> WorkResponseSchem:
        current_work: WorksORM | None = await self.dao.get_work_by_title(
            session=session, title=data_work.title
        )
        if current_work:
            raise WorkConflictException

        image_url: str | None = None
        if image:
            image_url: str = self.utils.save_image_from_work(image=image)

        new_work: WorksORM = await self.dao.create_work(
            session=session, data_work=data_work, image_url=image_url
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
            "price": data_work.price,
            "working_hour": data_work.working_hour,
        }

        result: WorksORM = await self.dao.patch_work_by_id(
            session=session, work=current_work, data_work=update_work
        )
        return WorkResponseSchem.model_validate(result)

    async def delete_work_by_id(
        self,
        session: AsyncSession,
        work_id: int,
    ) -> None:
        current_work: WorksORM | None = await self.dao.get_object_by_id(
            session=session, obj_id=work_id
        )
        if not current_work:
            raise WorkNotFoundException

        await self.dao.delete_work(session=session, current_work=current_work)
