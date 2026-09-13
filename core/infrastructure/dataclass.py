from dataclasses import dataclass


@dataclass(slots=True)
class CORSSettings:
    allow_origins: list[str]
    allow_methods: list[str]
    allow_headers: list[str]
    allow_credentials: bool
    expose_headers: list[str]
