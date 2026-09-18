from core.infrastructure.schemas import BaseSchem
from core.infrastructure.typing import INPUT_USER_DATE


class CreateWorkBookingSchem(BaseSchem):
    questionnaire_id: int
    work_id: int
    input_time: INPUT_USER_DATE
