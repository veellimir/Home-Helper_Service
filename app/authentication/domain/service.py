from datetime import UTC, datetime, timedelta
from email.message import EmailMessage

import aiosmtplib
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.domain.exceptions import (
    InvalidPasswordResetTokenException,
)
from app.authentication.infrastructure.dao import AuthDAO
from app.authentication.infrastructure.models import (
    PasswordResetTokenORM,
    RefreshTokenORM,
)
from app.authentication.infrastructure.schemes import (
    AccessTokenResponseSchem,
    LoginUserSchem,
    RegisterUserSchem,
    TokenResponseSchem,
)
from app.authentication.infrastructure.security import (
    PasswordService,
    TokenService,
)
from app.users.domain.exceptions import (
    UserConflictException,
    UserInputDataConflictException,
    UserInvalidCredentialsException,
    UsernameEmailNotNullException,
)
from app.users.infrastructure.dao import UsersDAO
from app.users.infrastructure.models import UsersORM
from core.config import settings
from core.domain.service import SQLAlchemyBaseService
from core.infrastructure.typing import utc_now


class AuthService(SQLAlchemyBaseService[UsersORM]):
    def __init__(self, dao: AuthDAO) -> None:
        self.dao = dao
        self.password_service = PasswordService()
        self.token_service = TokenService()
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

        await self.user_dao.create_user(
            session=session,
            password_service=self.password_service,
            user_data=user_data,
        )

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

        password_is_valid: bool = self.password_service.verify_password(
            password=user_data.password,
            password_hash=current_user.password_hash,
        )
        if not password_is_valid:
            raise UserInvalidCredentialsException

        access_token: str = self.token_service.create_access_token(
            user_id=current_user.id
        )

        refresh_token: str = self.token_service.create_refresh_token()
        refresh_token_hash: str = self.token_service.hash_refresh_token(
            refresh_token,
        )
        refresh_token_expiration = (
            self.token_service.get_refresh_token_expiration()
        )

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

    async def logout_user(
        self,
        session: AsyncSession,
        refresh_token: str,
    ) -> None:
        refresh_token_hash: str = self.token_service.hash_refresh_token(
            refresh_token,
        )

        stored_refresh_token: (
            RefreshTokenORM | None
        ) = await self.dao.get_refresh_token(
            session=session,
            token_hash=refresh_token_hash,
        )

        if stored_refresh_token is None:
            return

        await self.dao.revoke_refresh_token(
            session=session,
            refresh_token=stored_refresh_token,
        )

    async def refresh_access_token(
        self,
        session: AsyncSession,
        refresh_token: str,
    ) -> AccessTokenResponseSchem:
        refresh_token_hash: str = self.token_service.hash_refresh_token(
            refresh_token,
        )

        stored_refresh_token: (
            RefreshTokenORM | None
        ) = await self.dao.get_refresh_token(
            session=session,
            token_hash=refresh_token_hash,
        )

        if stored_refresh_token is None:
            raise UserInvalidCredentialsException

        if stored_refresh_token.expires_at <= datetime.now(UTC):
            raise UserInvalidCredentialsException

        access_token: str = self.token_service.create_access_token(
            user_id=stored_refresh_token.user_id,
        )

        return AccessTokenResponseSchem(
            access_token=access_token,
            token_type="bearer",
        )

    async def forgot_password(
        self, session: AsyncSession, email: EmailStr
    ) -> None:
        current_user = await self.user_dao.get_by_email(
            session=session, email=email
        )
        if not current_user:
            return

        token, token_hash = self.token_service.create_reset_token()

        expires_at = utc_now() + timedelta(
            minutes=settings.yandex.PASSWORD_RESET_EXPIRE_MINUTES
        )

        await self.dao.create_password_reset_token(
            session=session,
            user_id=current_user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        await self.send_password_reset_email(email=email, token=token)

    async def reset_password(
        self,
        session: AsyncSession,
        token: str,
        new_password: str,
    ) -> None:
        token_hash: str = self.token_service.hash_reset_token(token=token)

        reset_token: (
            PasswordResetTokenORM | None
        ) = await self.dao.get_password_reset_token(
            session=session,
            token_hash=token_hash,
        )
        if not reset_token:
            raise InvalidPasswordResetTokenException
        if reset_token.expires_at <= utc_now():
            raise InvalidPasswordResetTokenException

        current_user: UsersORM | None = await self.user_dao.get_user_by_id(
            session=session, user_id=reset_token.user_id
        )
        if not current_user:
            raise InvalidPasswordResetTokenException

        await self.dao.reset_password(
            session=session,
            user=current_user,
            new_password=new_password,
            reset_token=reset_token,
        )

    @staticmethod
    async def send_password_reset_email(
        email: str,
        token: str,
    ) -> None:
        reset_url: str = (
            f"{settings.yandex.FRONTEND_URL}/reset-password?token={token}"
        )

        message: EmailMessage = EmailMessage()

        message["From"] = settings.yandex.SMTP_FROM
        message["To"] = email
        message["Subject"] = "Восстановление пароля"

        message.set_content(
            "Вы запросили восстановление пароля.\n\n"
            "Для установки нового пароля перейдите по ссылке:\n\n"
            f"{reset_url}\n\n"
            f"Ссылка действительна "
            f"{settings.yandex.PASSWORD_RESET_EXPIRE_MINUTES} минут.\n\n"
            "Если вы не запрашивали восстановление пароля, "
            "просто проигнорируйте это письмо."
        )

        await aiosmtplib.send(
            message,
            hostname=settings.yandex.SMTP_HOST,
            port=settings.yandex.SMTP_PORT,
            username=settings.yandex.SMTP_USER,
            password=settings.yandex.SMTP_PASSWORD,
            use_tls=True,
        )
