from fastapi import HTTPException, status


class UnauthorizedNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )


class InvalidPasswordResetTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при сбросе токена",
        )
