from fastapi import HTTPException, status


class WorkBookingConflictException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Выбранное вами время недоступно, "
                "пожалуйста выберите другое доступное время"
            ),
        )


class BookingTimeConflictException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Выбранное недопустимое рабочее время,"
                "пожалуйста выберите любое доступное время с 8:00 до 20:00"
            ),
        )
