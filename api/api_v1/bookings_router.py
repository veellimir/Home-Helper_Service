from fastapi import APIRouter

from app.bookings.infrastructure.schemes import (
    CreateWorkBookingSchem,
    WorkBookingResponseSchem,
)
from core.config import settings
from dependecies.annotations import DBSessionDep, WorkBookingServiceDep

router = APIRouter(prefix=settings.api.v1.bookings, tags=["Booking Services"])


@router.get("/list", summary="Получить все вызовы мастера по времени")
async def get_list_work_bookings() -> None:
    """
    Получает список вызовов матера для каждого пользователя.

    :params None
    """
    pass


@router.post("/create", summary="Добавить запись по вызову мастера")
async def create_work_booking(
    session: DBSessionDep,
    service: WorkBookingServiceDep,
    data: CreateWorkBookingSchem,
) -> WorkBookingResponseSchem:
    """
    Создает вызов мастера по свободной дате и времени и выбранной работы.

    :questionnaire_id Уникальное идентификатор профиля пользователя \n
    :work_id Уникальный идентификатор выбранной работы \n
    :input_time Желаемое время заказчика (формат: 2026-09-20T16:00:00)
    """
    return await service.create_work_booking(
        session=session, booking_data=data
    )
