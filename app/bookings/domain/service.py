from app.bookings.domain.dao import WorkBookingDAO
from app.bookings.infrastructure.models import WorkBookingsORM
from core.domain.service import SQLAlchemyBaseService


class WorkBookingService(SQLAlchemyBaseService[WorkBookingsORM]):
    def __init__(self, dao: WorkBookingDAO) -> None:
        self.dao = dao
        super().__init__(self.dao)