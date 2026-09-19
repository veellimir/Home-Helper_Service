from core.infrastructure.schemas import BaseResponseSchem, BaseSchem
from core.infrastructure.typing import CustomDate


class WorkBookingResponseSchem(BaseResponseSchem):
    questionnaire_id: int
    work_id: int
    start_at: CustomDate
    end_at: CustomDate


class CreateWorkBookingSchem(BaseSchem):
    user_id: int
    work_id: int
    input_time: CustomDate
