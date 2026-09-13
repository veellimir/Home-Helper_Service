from pydantic import BaseModel

from core.infrastructure.schemas import BaseResponseSchem
from core.infrastructure.typing import CustomDate


class LessonsListResponseSchem(BaseResponseSchem):
    title: str


class LessonResponseSchem(LessonsListResponseSchem):
    start_date: CustomDate
    end_date: CustomDate
    description: str | None = None


class CreateLessonSchem(BaseModel):
    title: str
    start_date: CustomDate
    end_date: CustomDate
    description: str | None = None


class UpdateLessonSchem(CreateLessonSchem):
    pass
