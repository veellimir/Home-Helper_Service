from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.domain.dao import WorkBookingDAO
from app.bookings.infrastructure.models import WorkBookingsORM
from app.bookings.infrastructure.schemes import CreateWorkBookingSchem
from app.users.infrastructure.dao import UsersDAO
from app.works.infrastructure.dao import WorksDAO
from core.domain.service import SQLAlchemyBaseService


class WorkBookingService(SQLAlchemyBaseService[WorkBookingsORM]):
    def __init__(self, dao: WorkBookingDAO, works_dao: WorksDAO, users_dao: UsersDAO) -> None:
        self.dao = dao
        self.works_dao = works_dao
        self.users_dao = users_dao
        super().__init__(self.dao)

    async def create_work_booking(
        self, session: AsyncSession, booking_data: CreateWorkBookingSchem
    ):
        pass
