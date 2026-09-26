from typing import Annotated

from fastapi import Depends

from app.sse.manager import sse_manager
from app.sse.publisher import EventPublisher


def get_event_publisher() -> EventPublisher:
    return EventPublisher(
        sse_manager=sse_manager,
    )


EventPublisherDep = Annotated[
    EventPublisher,
    Depends(get_event_publisher),
]