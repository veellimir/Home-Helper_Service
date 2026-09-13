from sqlalchemy.ext.asyncio import AsyncSession

from core.infrastructure.dao import SQLAlchemyBaseDAO
from core.infrastructure.models import BaseORM


class SQLAlchemyBaseService[T: BaseORM]:
    def __init__(self, dao: SQLAlchemyBaseDAO[T]) -> None:
        self.dao = dao

    async def get_list(self, session: AsyncSession) -> None:
        pass
