import json

from app.sse.dataclass import WorkBookingDeletedEvent
from app.sse.manager import SSEManager


class EventPublisher:
    def __init__(
        self,
        sse_manager: SSEManager,
    ) -> None:
        self.sse_manager = sse_manager

    async def publish_work_booking_deleted(
        self,
        event: WorkBookingDeletedEvent,
    ) -> None:
        payload = json.dumps(
            {
                "event": "work_booking.deleted",
                "booking_id": event.booking_id,
                "user_id": event.user_id,
            }
        )

        await self.sse_manager.send_to_admins(payload)

    async def publish_work_booking_create(
        self,
        event: WorkBookingDeletedEvent,
    ) -> None:
        payload = json.dumps(
            {
                "event": "work_booking.create",
                "booking_id": event.booking_id,
                "user_id": event.user_id,
            }
        )

        await self.sse_manager.send_to_admins(payload)