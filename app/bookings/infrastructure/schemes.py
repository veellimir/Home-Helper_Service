from pydantic import computed_field

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


class CreateWorkBookingSchem(BaseSchem):
    user_id: int
    work_id: int
    input_time: CustomDate
