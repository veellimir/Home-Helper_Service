from enum import StrEnum, unique


@unique
class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"
    DEVELOPER = "developer"
