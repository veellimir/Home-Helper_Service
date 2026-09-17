from fastapi import APIRouter, status

from app.authentication.infrastructure.schemes import (
    AccessTokenResponseSchem,
    LoginUserSchem,
    LogoutRequestSchem,
    RefreshTokenRequestSchem,
    RegisterUserSchem,
    TokenResponseSchem,
)
from core.config import settings
from dependecies.annotations import AuthServiceDep, DBSessionDep

router = APIRouter(prefix=settings.api.v1.auth, tags=["Authenticated"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
    operation_id="register_user",
)
async def register_user(
    session: DBSessionDep,
    service: AuthServiceDep,
    user_data: RegisterUserSchem,
) -> None:
    """
    Регистрация нового пользователя \n
    Принимает уникальный username или email, а так же пароль.
    """
    return await service.register_user(
        session=session,
        user_data=user_data,
    )


@router.post(
    "/login", summary="Получить токен пользователя", operation_id="login_user"
)
async def login_user(
    session: DBSessionDep,
    service: AuthServiceDep,
    user_data: LoginUserSchem,
) -> TokenResponseSchem:
    """
    Авторизация пользователя по username или email.
    """
    return await service.login_user(session=session, user_data=user_data)


@router.post(
    "/refresh", summary="Обновить access токен", operation_id="refresh_token"
)
async def refresh(
    session: DBSessionDep,
    service: AuthServiceDep,
    data: RefreshTokenRequestSchem,
) -> AccessTokenResponseSchem:
    """
    Обновление access токена по refresh.

    :refresh_token Принимает \n
    -> access_token
    """
    return await service.refresh_access_token(
        session=session,
        refresh_token=data.refresh_token,
    )


@router.post(
    "/logout",
    summary="Выйти из аккаунта",
    status_code=status.HTTP_200_OK,
    operation_id="logout_user",
)
async def logout_user(
    session: DBSessionDep,
    service: AuthServiceDep,
    data: LogoutRequestSchem,
) -> None:
    """
    Выйти из аккаунта и деактивировать токен пользователя.
    """
    await service.logout_user(
        session=session,
        refresh_token=data.refresh_token,
    )
