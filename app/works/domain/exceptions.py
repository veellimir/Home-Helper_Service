from fastapi import HTTPException, status


class WorkNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )
