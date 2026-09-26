from pydantic import computed_field

from app.bookings.domain.enums import StatusBookingEnum
from app.users.infrastructure.schemes import QuestionnaireResponseSchem
from core.infrastructure.schemas import BaseResponseSchem, BaseSchem
from core.infrastructure.typing import CustomDate


class WorkBookingResponseSchem(BaseResponseSchem):
    questionnaire_id: int
    work_id: int
    start_at: CustomDate
    end_at: CustomDate


class WorkBookingListShem(BaseSchem):
    id: int
    work_id: int
    status: StatusBookingEnum
    comment: str | None = None
    start_at: CustomDate
    end_at: CustomDate

    @computed_field
    def weekday(self) -> str:
        days = (
            "понедельник",
            "вторник",
            "среда",
            "четверг",
            "пятница",
            "суббота",
            "воскресенье",
        )
        return days[self.start_at.weekday()]


class WorkBookingSchem(WorkBookingListShem):
    pass


class WorkBookingDetailListShem(WorkBookingListShem):
    questionnaire: QuestionnaireResponseSchem


class UpdateWorkBooking(BaseSchem):
    status: StatusBookingEnum
    comment: str | None = None


class CreateWorkBookingSchem(BaseSchem):
    work_id: int
    input_time: CustomDate


class DeleteWorkBookingSchem(BaseSchem):
    work_booking_id: int
