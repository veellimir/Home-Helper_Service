from core.infrastructure.dao import SQLAlchemyBaseDAO


class WorkBookingDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = WorkBookingDAO
        super().__init__(WorkBookingDAO)
