from fastapi import APIRouter

from app.works.infrastructure.schemes import (
    CreateWorkSchem,
    UpdateWorkSchem,
    WorkResponseSchem,
    WorksListResponseSchem,
)
from core.config import settings
from dependecies.annotations import (
    DBSessionDep,
    WorksServiceDep,
)

router = APIRouter(prefix=settings.api.v1.works, tags=["Услуги работ"])


@router.get("/list", summary="Получить список услуг")
async def get_list_works(
    session: DBSessionDep, service: WorksServiceDep
) -> list[WorksListResponseSchem]:
    return await service.get_list_works(session=session)


@router.get("/{work_id}", summary="Получить услугу по ID")
async def get_work_by_id(
    session: DBSessionDep, service: WorksServiceDep, work_id: int
) -> WorkResponseSchem | None:
    return await service.get_work_by_id(session=session, work_id=work_id)


@router.post("/create", summary="Создание услугу")
async def create_work(
    session: DBSessionDep,
    service: WorksServiceDep,
    data: CreateWorkSchem,
) -> WorkResponseSchem:
    return await service.create_work(session=session, data_work=data)


@router.patch("/{work_id}", summary="Обновить услугу по ID")
async def patch_work_by_id(
    session: DBSessionDep,
    service: WorksServiceDep,
    work_id: int,
    data: UpdateWorkSchem,
) -> WorkResponseSchem | None:
    return await service.patch_work_by_id(
        session=session, work_id_id=work_id, data_work=data
    )


@router.delete("/{work_id}", summary="Удаление услуги")
async def delete_work_by_id(
    session: DBSessionDep,
    service: WorksServiceDep,
    work_id: int,
) -> None:
    return await service.delete_work_by_id(session=session, work_id=work_id)
