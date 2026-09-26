from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.authentication.dependencies.current_user import CurrentUserDep
from app.sse.manager import sse_manager
from app.users.domain.enums import UserRoleEnum
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.notifications, tags=["Notifications"]
)


@router.get("/events", summary="Получение событий")
async def events(user: CurrentUserDep) -> StreamingResponse:
    """
    Уведомления для администратора сервиса. \n

    Быстрая проверка: http://127.0.0.1:8000/api/v1/notifications/events

    :param user:
    :return: Message
    """
    if user.role != UserRoleEnum.ADMIN:
        return None

    return StreamingResponse(
        sse_manager.connect_admin(),
        media_type="text/event-stream",
    )
