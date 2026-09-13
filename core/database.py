import json
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import settings

engine = create_async_engine(
    settings.db.DATABASE_URL,
    echo=settings.db.ECHO_LOG,
    json_serializer=lambda obj: json.dumps(
        obj, ensure_ascii=False, default=str
    ),
)

async_session_maker = async_sessionmaker(
    bind=engine, expire_on_commit=True, autoflush=True
)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker.begin() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
