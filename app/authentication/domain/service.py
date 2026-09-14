from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.infrastructure.dao import AuthDAO
from app.authentication.infrastructure.schemes import (
    AccessTokenResponseSchem,
    LoginUserSchem,
    RegisterUserSchem,
    TokenResponseSchem,
)
from app.authentication.infrastructure.security import (
    create_access_token,
    create_refresh_token,
    get_refresh_token_expiration,
    hash_refresh_token,
    verify_password,
)
from app.users.domain.exceptions import (
    UserConflictException,
    UserInputDataConflictException,
    UserInvalidCredentialsException,
    UsernameEmailNotNullException,
)
from app.users.infrastructure.dao import UsersDAO
from app.users.infrastructure.models import UsersORM
from core.domain.service import SQLAlchemyBaseService


class AuthService(SQLAlchemyBaseService[UsersORM]):
    def __init__(self, dao: AuthDAO) -> None:
        self.dao = dao
        self.user_dao = UsersDAO()
        super().__init__(self.dao)

    async def register_user(
        self, session: AsyncSession, user_data: RegisterUserSchem
    ) -> None:
        if not user_data.username and not user_data.email:
            raise UsernameEmailNotNullException

        current_username: bool = False
        current_email: bool = False

        if user_data.username:
            current_username: (
                UsersORM | None
            ) = await self.user_dao.get_by_username(
                session=session, username=user_data.username
            )
        if user_data.email:
            current_email: UsersORM | None = await self.user_dao.get_by_email(
                session=session, email=user_data.email
            )

        if current_username or current_email:
            raise UserConflictException

        await self.user_dao.create_user(session=session, user_data=user_data)

    async def login_user(
        self, session: AsyncSession, user_data: LoginUserSchem
    ) -> TokenResponseSchem:
        if user_data.username is None and user_data.email is None:
            raise UserInputDataConflictException

        current_user: UsersORM | None = None

        if user_data.username is not None:
            current_user: (
                UsersORM | None
            ) = await self.user_dao.get_by_username(
                session=session, username=user_data.username
            )
        elif user_data.email is not None:
            current_user: UsersORM | None = await self.user_dao.get_by_email(
                session=session, email=user_data.email
            )

        if current_user is None:
            raise UserInvalidCredentialsException

        password_is_valid: bool = verify_password(
            password=user_data.password,
            password_hash=current_user.password_hash,
        )
        if not password_is_valid:
            raise UserInvalidCredentialsException

        access_token: str = create_access_token(user_id=current_user.id)

        refresh_token: str = create_refresh_token()
        refresh_token_hash: str = hash_refresh_token(
            refresh_token,
        )
        refresh_token_expiration = get_refresh_token_expiration()

        await self.dao.create_refresh_token(
            session=session,
            user_id=current_user.id,
            token_hash=refresh_token_hash,
            expires_at=refresh_token_expiration,
        )

        return TokenResponseSchem(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_access_token(
        self,
        session: AsyncSession,
        refresh_token: str,
    ) -> AccessTokenResponseSchem:
        refresh_token_hash = hash_refresh_token(
            refresh_token,
        )

        stored_refresh_token = await self.dao.get_refresh_token(
            session=session,
            token_hash=refresh_token_hash,
        )

        if stored_refresh_token is None:
            raise UserInvalidCredentialsException

        if stored_refresh_token.expires_at <= datetime.now(UTC):
            raise UserInvalidCredentialsException

        access_token = create_access_token(
            user_id=stored_refresh_token.user_id,
        )

        return AccessTokenResponseSchem(
            access_token=access_token,
            token_type="bearer",
        )
