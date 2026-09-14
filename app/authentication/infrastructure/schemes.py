from pydantic import BaseModel, EmailStr, Field

from core.infrastructure.schemas import BaseSchem


class RegisterUserSchem(BaseSchem):
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


class LoginUserSchem(BaseSchem):
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


class LogoutUserSchem(BaseSchem):
    refresh_token: str


class TokenResponseSchem(BaseSchem):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenSchem(BaseSchem):
    refresh_token: str


class RefreshTokenRequestSchem(BaseModel):
    refresh_token: str


class AccessTokenResponseSchem(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LogoutRequestSchem(RefreshTokenRequestSchem):
    pass
