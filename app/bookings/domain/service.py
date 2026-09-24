from datetime import datetime, time, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.domain.exceptions import (
    BookingTimeConflictException,
    WorkBookingConflictException,
)
from app.bookings.infrastructure.dao import WorkBookingDAO
from app.bookings.infrastructure.models import WorkBookingsORM
from app.bookings.infrastructure.schemes import (
    CreateWorkBookingSchem,
    WorkBookingListShem,
    WorkBookingResponseSchem,
)
from app.users.domain.exceptions import QuestionnaireNotFoundException
from app.users.domain.service import UsersService
from app.users.infrastructure.schemes import UserResponseSchem
from app.works.domain.service import WorksService
from app.works.infrastructure.schemes import WorkResponseSchem
from core.domain.service import SQLAlchemyBaseService


class WorkBookingService(SQLAlchemyBaseService[WorkBookingsORM]):
    def __init__(
        self,
        dao: WorkBookingDAO,
        works_service: WorksService,
        users_service: UsersService,
    ) -> None:
        self.dao = dao
        self.works_service = works_service
        self.users_service = users_service
        super().__init__(self.dao)

    async def get_list_work_bookings(
        self,
        session: AsyncSession,
    ) -> list[WorkBookingListShem]:
        bookings: WorkBookingService = await self.dao.get_list_work_bookings(
            session=session
        )

        return [
            WorkBookingListShem.model_validate(booking)
            for booking in bookings
        ]

    async def create_work_booking(
        self,
        session: AsyncSession,
        booking_data: CreateWorkBookingSchem,
        user_id: int,
    ) -> None:
        current_work: (
            WorkResponseSchem | None
        ) = await self.works_service.get_work_by_id(
            session=session, work_id=booking_data.work_id
        )
        current_user: (
            UserResponseSchem | None
        ) = await self.users_service.get_user_by_id(
            session=session, user_id=user_id
        )
        if not current_user.questionnaire:
            raise QuestionnaireNotFoundException

        end_at: datetime = self._time_calculation(
            booking_data=booking_data, current_work=current_work
        )
        work_time_check: bool = self._work_time_checking(
            start_at=booking_data.input_time, end_at=end_at
        )
        if work_time_check is False:
            raise BookingTimeConflictException

        current_booking: list[
            WorkBookingsORM
        ] = await self.dao.get_work_booking_by_datetime(
            session=session, start_at=booking_data.input_time, end_at=end_at
        )
        if current_booking:
            raise WorkBookingConflictException

        new_booking: WorkBookingDAO = await self.dao.create_booking(
            session=session,
            work_id=current_work.id,
            questionnaire_id=current_user.questionnaire.id,
            start_at=booking_data.input_time,
            end_at=end_at,
        )
        return WorkBookingResponseSchem.model_validate(new_booking)

    async def delete_work_booking(self) -> None:
        pass

    @staticmethod
    def _time_calculation(
        booking_data: CreateWorkBookingSchem, current_work: WorkResponseSchem
    ) -> datetime:
        return booking_data.input_time + timedelta(
            hours=current_work.working_hour
        )

    @staticmethod
    def _work_time_checking(start_at: datetime, end_at: datetime) -> bool:
        work_start = time(8, 0)
        work_end = time(20, 0)

        return start_at.time() >= work_start and end_at.time() <= work_end
