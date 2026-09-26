from enum import StrEnum, unique


@unique
class StatusBookingEnum(StrEnum):
    WAITING = "waiting"
    ACCEPTED = "accepted",
    EDITING = "editing"
    CANCELLED = "cancelled"
