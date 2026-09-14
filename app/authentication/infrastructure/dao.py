from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.infrastructure.models import RefreshTokenORM, UsersORM
from core.infrastructure.dao import SQLAlchemyBaseDAO


class AuthDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = UsersORM
        super().__init__(UsersORM)

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
    async def revoke_refresh_token(
        session: AsyncSession,
        refresh_token: RefreshTokenORM,
    ) -> None:
        refresh_token.revoker_at = datetime.now(UTC)
        await session.flush()
