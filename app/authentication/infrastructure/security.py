import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from core.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Хеширует пароль перед сохранением в базу данных.
    """
    return password_hasher.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Проверяет введённый пароль относительно сохранённого хеша.
    """
    return password_hasher.verify(
        password,
        password_hash,
    )


def create_access_token(
    user_id: int,
) -> str:
    """
    Создаёт JWT access-токен пользователя.
    """
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.auth.JWT_SECRET_KEY,
        algorithm=settings.auth.JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Декодирует и проверяет JWT access-токен.

    Выбрасывает InvalidTokenError, если токен:
    - повреждён;
    - подписан неправильным ключом;
    - просрочен;
    - имеет некорректную структуру.
    """
    return jwt.decode(
        token,
        settings.auth.JWT_SECRET_KEY,
        algorithms=[settings.auth.JWT_ALGORITHM],
    )


def get_user_id_from_access_token(
    token: str,
) -> int:
    """
    Извлекает идентификатор пользователя из access-токена.
    """
    try:
        payload = decode_access_token(token)

    except ExpiredSignatureError as exc:
        raise InvalidTokenError("Access-токен просрочен") from exc

    except InvalidTokenError as exc:
        raise InvalidTokenError("Некорректный access-токен") from exc

    if payload.get("type") != "access":
        raise InvalidTokenError("Недопустимый тип токена")

    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidTokenError(
            "B access-токене отсутствует идентификатор пользователя",
        )

    try:
        return int(user_id)

    except (TypeError, ValueError) as exc:
        raise InvalidTokenError(
            "Некорректный идентификатор пользователя",
        ) from exc


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_refresh_token(
    token: str,
) -> str:
    """
    Создаёт хеш refresh-токена.
    """
    return hashlib.sha256(
        token.encode("utf-8"),
    ).hexdigest()


def get_refresh_token_expiration() -> datetime:
    """
    Возвращает дату и время истечения refresh-токена.
    """
    return datetime.now(UTC) + timedelta(
        days=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS,
    )
