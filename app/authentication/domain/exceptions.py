from fastapi import HTTPException, status


class InvalidPasswordResetTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при сбросе токена",
        )
