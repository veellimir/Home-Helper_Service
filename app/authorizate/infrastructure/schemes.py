from pydantic import EmailStr, Field

from core.infrastructure.schemas import BaseSchem


class RegisterSchema(BaseSchem):
    username: str | None = Field(
        default=None,
        min_length=5,
        max_length=20,
    )

    email: EmailStr | None = None

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class LoginSchema(BaseSchem):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=20,
    )

    email: EmailStr | None = None

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class TokenResponseSchema(BaseSchem):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshSchema(BaseSchem):
    refresh_token: str


class LogoutSchema(BaseSchem):
    refresh_token: str