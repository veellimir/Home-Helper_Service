from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.infrastructure.models import (
    PasswordResetTokenORM,
    RefreshTokenORM,
)
from app.authentication.infrastructure.security import PasswordService
from app.users.infrastructure.models import UsersORM
from core.infrastructure.dao import SQLAlchemyBaseDAO
from core.infrastructure.typing import CustomDate, utc_now


class AuthDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.password_service = PasswordService()
        self.model = UsersORM
        super().__init__(UsersORM)

    @staticmethod
    async def get_password_reset_token(
        session: AsyncSession, token_hash: str
    ) -> PasswordResetTokenORM | None:
        stmt = select(PasswordResetTokenORM).where(
            PasswordResetTokenORM.token_hash == token_hash,
            PasswordResetTokenORM.used_at.is_(None),
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_refresh_token(
        session: AsyncSession,
        token_hash: str,
    ) -> RefreshTokenORM | None:
        stmt = select(RefreshTokenORM).where(
            RefreshTokenORM.token_hash == token_hash,
            RefreshTokenORM.revoker_at.is_(None),
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_refresh_token(
        session: AsyncSession,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshTokenORM:
        refresh_token = RefreshTokenORM(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        session.add(refresh_token)
        await session.flush()
        return refresh_token

    @staticmethod
    async def create_password_reset_token(
        session: AsyncSession,
        user_id: int,
        token_hash: str,
        expires_at: CustomDate,
    ) -> PasswordResetTokenORM:
        reset_token = PasswordResetTokenORM(
            user_id=user_id, token_hash=token_hash, expires_at=expires_at
        )
        session.add(reset_token)
        await session.flush()

        return reset_token

    async def reset_password(
        self,
        session: AsyncSession,
        user: UsersORM,
        new_password: str,
        reset_token: PasswordResetTokenORM,
    ) -> None:
        user.password_hash: str = self.password_service.hash_password(
            password=new_password
        )
        reset_token.used_at = utc_now()

        await session.flush()

    @staticmethod
    async def revoke_user_refresh_tokens(
        session: AsyncSession,
        user_id: int,
    ) -> None:
        stmt = (
            update(RefreshTokenORM)
            .where(
                RefreshTokenORM.user_id == user_id,
                RefreshTokenORM.revoker_at.is_(None),
            )
            .values(
                revoked_at=utc_now(),
            )
        )
        await session.execute(stmt)

    @staticmethod
    async def revoke_refresh_token(
        session: AsyncSession,
        refresh_token: RefreshTokenORM,
    ) -> None:
        refresh_token.revoker_at = datetime.now(UTC)
        await session.flush()
