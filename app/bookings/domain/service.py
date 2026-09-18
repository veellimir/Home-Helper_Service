from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.domain.exceptions import WorkBookingConflictException
from app.bookings.infrastructure.dao import WorkBookingDAO
from app.bookings.infrastructure.models import WorkBookingsORM
from app.bookings.infrastructure.schemes import CreateWorkBookingSchem
from app.users.domain.exceptions import QuestionnaireNotFoundException
from app.users.domain.service import UsersService
from app.users.infrastructure.schemes import UserResponseSchem
from app.works.domain.service import WorksService
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

    async def create_work_booking(
        self, session: AsyncSession, booking_data: CreateWorkBookingSchem
    ) -> None:
        await self.works_service.get_work_by_id(
            session=session, work_id=booking_data.work_id
        )
        current_user: (
            UserResponseSchem | None
        ) = await self.users_service.get_user_by_id(
            session=session, user_id=booking_data.user_id
        )
        if not current_user.questionnaire:
            raise QuestionnaireNotFoundException

        current_booking = await self.dao.get_work_booking_by_datetime(
            session=session, booking_date=booking_data.input_time
        )
        if current_booking:
            raise WorkBookingConflictException
