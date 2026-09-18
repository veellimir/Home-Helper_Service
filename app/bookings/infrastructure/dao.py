from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.infrastructure.models import WorkBookingsORM
from core.infrastructure.dao import SQLAlchemyBaseDAO
from core.infrastructure.typing import INPUT_USER_DATE


class WorkBookingDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = WorkBookingsORM
        super().__init__(WorkBookingsORM)

    async def get_work_booking_by_datetime(
        self, session: AsyncSession, booking_date: INPUT_USER_DATE
    ) -> WorkBookingsORM | None:
        stmt = select(self.model).where(self.model.start_at == booking_date)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
