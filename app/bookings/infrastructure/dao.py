from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.bookings.infrastructure.models import WorkBookingsORM
from app.bookings.infrastructure.schemes import UpdateWorkBooking
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
    ) -> WorkBookingsORM:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.questionnaire))
            .order_by(self.model.start_at)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_work_booking_by_id(
        self, session: AsyncSession, work_booking_id: int
    ) -> WorkBookingsORM | None:
        stmt = select(self.model).where(self.model.id == work_booking_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

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

    async def update_status(
        self,
        session: AsyncSession,
        current_booking: WorkBookingsORM,
        booking_data: UpdateWorkBooking,
    ) -> WorkBookingsORM:
        if booking_data.status:
            current_booking.comment = booking_data.comment
        current_booking.status = booking_data.status

        await session.flush()
        return current_booking

    async def delete_work_booking(
        self, session: AsyncSession, current_booking: WorkBookingsORM
    ) -> None:
        await session.delete(current_booking)
        await session.flush()
