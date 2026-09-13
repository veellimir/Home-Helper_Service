from pydantic import BaseModel, ConfigDict

from core.infrastructure.typing import CustomDate


class BaseSchem(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchem(BaseSchem):
    id: int
    created_at: CustomDate
    update_at: CustomDate
