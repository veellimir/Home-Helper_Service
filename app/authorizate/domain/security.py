import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from core.config import settings

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    return password_hasher.verify(
        password,
        password_hash,
    )


def create_access_token(
    user_id: int,
) -> str:
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


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(
        token.encode(),
    ).hexdigest()


def get_refresh_token_expiration() -> datetime:
    return datetime.now(UTC) + timedelta(
        days=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.auth.JWT_SECRET_KEY,
        algorithms=[settings.auth.JWT_ALGORITHM],
    )
