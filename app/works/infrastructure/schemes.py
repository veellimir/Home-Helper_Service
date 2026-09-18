from pydantic import BaseModel

from core.infrastructure.schemas import BaseResponseSchem


class WorksListResponseSchem(BaseResponseSchem):
    title: str
    image_url: str | None = None


class WorkResponseSchem(WorksListResponseSchem):
    price: int
    description: str
    working_hour: int


class CreateWorkSchem(BaseModel):
    title: str
    description: str
    price: int
    working_hour: int


class UpdateWorkSchem(CreateWorkSchem):
    pass
