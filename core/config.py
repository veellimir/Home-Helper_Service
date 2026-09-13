from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from core.domain.constant import env, env_file
from core.infrastructure.dataclass import CORSSettings


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DataBase(BaseSettings):
    DATABASE_URL: str
    ECHO_LOG: bool

    class Config:
        env_prefix = ""


class ApiV1Prefix(BaseModel):
    prefix: str = "/api/v1"

    auth: str = "/auth"
    users: str = "/users"
    works: str = "/works"


class ApiPrefix(BaseModel):
    v1: ApiV1Prefix = ApiV1Prefix()


class AuthConfig(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="allow",
    )

    # Configs
    run: RunConfig = RunConfig()
    db: DataBase
    api: ApiPrefix = ApiPrefix()
    auth: AuthConfig

    ENV: str = env

    @property
    def cors(self) -> CORSSettings:
        return CORSSettings(
            allow_origins=["*", f"http://localhost:{self.run.port}"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["X-Total-Count"],
        )


settings = Settings()
