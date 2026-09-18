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
