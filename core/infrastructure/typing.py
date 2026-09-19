from datetime import UTC, datetime
from typing import Annotated

from fastapi import Query
from pydantic import PlainSerializer
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column


# NOTE: From models
def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


CREATED_AT = Annotated[
    datetime,
    mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    ),
]

UPDATE_AT = Annotated[
    datetime,
    mapped_column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    ),
]

INPUT_USER_DATE = Annotated[datetime, mapped_column(DateTime)]

INT_PK = Annotated[
    int,
    mapped_column(primary_key=True),
]


# NOTE: From Schemas
def serialize_datetime(value: datetime) -> str:
    return value.strftime("%d.%m.%Y %H:%M")


CustomDate = Annotated[
    datetime,
    PlainSerializer(
        serialize_datetime,
        return_type=str,
    ),
]

PAGINATION_FIELD: int = Query(default=20, ge=1, le=100)
