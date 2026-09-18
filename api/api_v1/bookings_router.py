from fastapi import APIRouter

from core.config import settings


router = APIRouter(prefix=settings.api.v1.bookings, tags=["Booking Services"])


@router.get("/list", summary="Получить все вызовы мастера по времени")
async def get_list_work_bookings(

):
    """
    Получает список вызовов матера для каждого пользователя.

    :params None
    """
    pass


@router.post("/create", summary="Добавить запись по вызову мастера")
async def create_work_booking(
) :
    """
    Создает вызов мастера по свободной дате и времени и выбранной работы.

    :? Уникальное Название услуги \n

    """
    pass