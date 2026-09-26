from fastapi import APIRouter

from app.authentication.dependencies.current_user import CurrentUserDep
from app.bookings.infrastructure.schemes import (
    CreateWorkBookingSchem,
    DeleteWorkBookingSchem,
    WorkBookingDetailListShem,
    WorkBookingListShem,
    WorkBookingResponseSchem,
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


@router.get("/list-detail", summary="Получить все вызовы пользователей")
async def get_list_detail_work_bookings(
    session: DBSessionDep,
    service: WorkBookingServiceDep,
) -> list[WorkBookingDetailListShem]:
    """
    Получает список вызовов пользователей.

    :params None
    """
    return await service.get_list_detail_work_bookings(session=session)


@router.post("/create", summary="Добавить запись по вызову мастера")
async def create_work_booking(
    session: DBSessionDep,
    service: WorkBookingServiceDep,
    user: CurrentUserDep,
    data: CreateWorkBookingSchem,
) -> WorkBookingResponseSchem:
    """
    Создает вызов мастера по свободной дате и времени и выбранной работы.

    В будущем будет приходить уведомление по SSE

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
    user: CurrentUserDep,
    data: DeleteWorkBookingSchem,
) -> None:
    """
    Удаляет вызов мастера если запись существует.

    В будущем будет приходить уведомление по SSE

    :work_booking_id Уникальный идентификатор выбранной работы \n
    """

    return await service.delete_work_booking(
        session=session, user_id=user.id, booking_data=data
    )
