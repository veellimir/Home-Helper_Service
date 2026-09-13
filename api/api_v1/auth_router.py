from fastapi import APIRouter, status

from app.authentication.infrastructure.schemes import RegisterUserSchem
from core.config import settings
from dependecies.annotations import AuthServiceDep, DBSessionDep

router = APIRouter(prefix=settings.api.v1.auth, tags=["Аутентификация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    session: DBSessionDep,
    service: AuthServiceDep,
    user_data: RegisterUserSchem,
) -> None:
    """
    Регистрация нового пользователя.
    Принимает username или email и пароль.
    """
    return await service.register_user(
        session=session,
        user_data=user_data,
    )
