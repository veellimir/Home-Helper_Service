from fastapi import APIRouter

from app.authentication.dependencies.current_user import CurrentUserDep
from app.bookings.infrastructure.schemes import (
    CreateWorkBookingSchem,
    WorkBookingListShem,
    WorkBookingResponseSchem, DeleteWorkBookingSchem,
)
from core.config import settings
from dependecies.annotations import DBSessionDep, WorkBookingServiceDep

router = APIRouter(prefix=settings.api.v1.bookings, tags=["Booking Services"])


@router.get("/list", summary="Получить все вызовы мастера по времени")
async def get_list_work_bookings(
    session: DBSessionDep,
    service: WorkBookingServiceDep,
) -> list[WorkBookingListShem]:
    """
    Получает список занятых дней и времени.

    :params None
    """
    return await service.get_list_work_bookings(session=session)


@router.post("/create", summary="Добавить запись по вызову мастера")
async def create_work_booking(
    session: DBSessionDep,
    service: WorkBookingServiceDep,
    data: CreateWorkBookingSchem,
    user: CurrentUserDep,
) -> WorkBookingResponseSchem:
    """
    Создает вызов мастера по свободной дате и времени и выбранной работы.

    :work_id Уникальный идентификатор выбранной работы \n
    :input_time Желаемое время заказчика (формат: 2026-09-20T16:00:00)
    """
    return await service.create_work_booking(
        session=session, booking_data=data, user_id=user.id
    )


@router.delete("/delete", summary="Отменить вызов мастера")
async def delete_work_booking(
    session: DBSessionDep,
    service: WorkBookingServiceDep,
    data: DeleteWorkBookingSchem,
    user: CurrentUserDep,
) -> None:
    """
    Маршрут в разработке !!

    Удаляет вызов мастера если запись существует.

    :work_id Уникальный идентификатор выбранной работы \n
    :input_time Текущее время вызова (формат: 2026-09-20T16:00:00)
    """
    return await service.delete_work_booking(
        session=session,
    )