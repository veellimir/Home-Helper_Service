from datetime import datetime
from typing import Annotated

from pydantic import PlainSerializer
from sqlalchemy import DateTime, text
from sqlalchemy.orm import mapped_column


# NOTE: From models
def utc_now() -> datetime:
    return datetime.now().astimezone().replace(tzinfo=None)


CREATED_AT = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', 'now')"),
    ),
]

UPDATE_AT = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', 'now')"),
        onupdate=utc_now,
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
