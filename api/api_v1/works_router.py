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

router = APIRouter(prefix=settings.api.v1.works, tags=["Services"])


@router.get("/list", summary="Получить список услуг")
async def get_list_works(
    session: DBSessionDep, service: WorksServiceDep
) -> list[WorksListResponseSchem]:
    """
    Получает список доступных услуг

    :params None
    """
    return await service.get_list_works(session=session)


@router.get("/{work_id}", summary="Получить услугу по ID")
async def get_work_by_id(
    session: DBSessionDep, service: WorksServiceDep, work_id: int
) -> WorkResponseSchem | None:
    """
    Получает подробную информацию по выбранной услуге

    :work_id Идентификатор услуги
    """
    return await service.get_work_by_id(session=session, work_id=work_id)


@router.post("/create", summary="Создание услуги")
async def create_work(
    session: DBSessionDep,
    service: WorksServiceDep,
    data: CreateWorkSchem,
) -> WorkResponseSchem:
    """
    Создает услугу с уникальным названием

    :title Уникальное Название услуги \n
    :description Подробное описание услуги \n
    :price Цена за услугу \n
    :working_hour Время проводимых работ \n
    """
    return await service.create_work(session=session, data_work=data)


@router.patch("/{work_id}", summary="Обновить услугу по ID")
async def patch_work_by_id(
    session: DBSessionDep,
    service: WorksServiceDep,
    work_id: int,
    data: UpdateWorkSchem,
) -> WorkResponseSchem | None:
    """
    Обновляет выбранную услугу

    :title Уникальное Название услуги \n
    :description Подробное описание услуги \n
    :price Цена за услугу \n
    :working_hour Время проводимых работ \n
    """
    return await service.patch_work_by_id(
        session=session, work_id=work_id, data_work=data
    )


@router.delete("/{work_id}", summary="Удаление услуги")
async def delete_work_by_id(
    session: DBSessionDep,
    service: WorksServiceDep,
    work_id: int,
) -> None:
    """
    Удаляет выбранную услугу

    :work_id Идентификатор услуги
    """
    return await service.delete_work_by_id(session=session, work_id=work_id)
