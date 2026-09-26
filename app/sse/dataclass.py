from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkBookingEvent:
    booking_id: int
    user_id: int
