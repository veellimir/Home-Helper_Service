from pydantic import BaseModel

from core.infrastructure.schemas import BaseResponseSchem
from core.infrastructure.typing import CustomDate


class WorksListResponseSchem(BaseResponseSchem):
    title: str


class WorkResponseSchem(WorksListResponseSchem):
    start_date: CustomDate
    end_date: CustomDate
    description: str | None = None


class CreateWorkSchem(BaseModel):
    title: str
    start_date: CustomDate
    end_date: CustomDate
    description: str | None = None


class UpdateWorkSchem(CreateWorkSchem):
    pass
