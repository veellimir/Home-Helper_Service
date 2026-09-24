from datetime import datetime
from typing import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.bookings.infrastructure.models import WorkBookingsORM
from app.users.infrastructure.models import UsersORM
from core.infrastructure.dao import SQLAlchemyBaseDAO


class WorkBookingDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = WorkBookingsORM
        super().__init__(WorkBookingsORM)

    async def get_work_booking_by_datetime(
        self, session: AsyncSession, start_at: datetime, end_at: datetime
    ) -> list[WorkBookingsORM]:
        stmt = select(self.model).where(
            and_(
                self.model.start_at < end_at,
                self.model.end_at > start_at,
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_list_work_bookings(
        self,
        session: AsyncSession,
    ) -> WorkBookingsORM:
        stmt = select(self.model).order_by(self.model.start_at)

        result = await session.execute(stmt)
        return result.scalars().all()


    async def get_list_detail_work_bookings(
        self,
        session: AsyncSession,
    ) -> list[WorkBookingsORM]:
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.questionnaire)
            )
            .order_by(self.model.start_at)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    async def create_booking(
        self,
        session: AsyncSession,
        work_id: int,
        questionnaire_id: int,
        start_at: datetime,
        end_at: datetime,
    ) -> WorkBookingsORM:
        new_booking = self.model(
            questionnaire_id=questionnaire_id,
            work_id=work_id,
            start_at=start_at,
            end_at=end_at,
        )

        session.add(new_booking)
        await session.flush()

        return new_booking
