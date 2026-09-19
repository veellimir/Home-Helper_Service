from typing import Annotated

from fastapi import APIRouter, File, Form, Response, UploadFile

from app.works.infrastructure.schemes import (
    WorkResponseSchem,
    WorksPaginationResponseSchem,
)
from core.config import settings
from core.infrastructure.typing import PAGINATION_FIELD
from dependecies.annotations import (
    DBSessionDep,
    WorksServiceDep,
)

router = APIRouter(prefix=settings.api.v1.works, tags=["Services"])


@router.get("/list", summary="Получить список услуг")
async def get_list_works(
    session: DBSessionDep,
    service: WorksServiceDep,
    response: Response,
    limit: int = PAGINATION_FIELD,
    cursor: int | None = None,
) -> WorksPaginationResponseSchem:
    """
    Получает список доступных услуг

    :limit Максимальный лимит загрузки за один раз (default=20) \n
    :cursor Точка с которой продолжить загрузку
    """
    result, total = await service.get_list_works_with_filters(
        session=session, limit=limit, cursor=cursor
    )
    response.headers["X-Total-Count"] = str(total)

    return result


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
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    price: Annotated[int, Form()],
    working_hour: Annotated[int, Form()],
    image: Annotated[UploadFile | None, File()] = None,
) -> WorkResponseSchem:
    """
    Создает услугу с уникальным названием

    :title Уникальное Название услуги \n
    :description Подробное описание услуги \n
    :price Цена за услугу \n
    :working_hour Время проводимых работ \n
    """
    return await service.create_work(
        session=session,
        title=title,
        description=description,
        price=price,
        working_hour=working_hour,
        image=image,
    )


@router.patch("/{work_id}", summary="Обновить услугу по ID")
async def patch_work_by_id(
    session: DBSessionDep,
    service: WorksServiceDep,
    work_id: int,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    price: Annotated[int, Form()],
    working_hour: Annotated[int, Form()],
    image: Annotated[UploadFile | None, File()] = None,
) -> WorkResponseSchem | None:
    """
    Обновляет выбранную услугу

    :title Уникальное Название услуги \n
    :description Подробное описание услуги \n
    :price Цена за услугу \n
    :working_hour Время проводимых работ \n
    """
    return await service.patch_work_by_id(
        session=session,
        work_id=work_id,
        title=title,
        description=description,
        price=price,
        working_hour=working_hour,
        image=image,
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
