from enum import StrEnum, unique


@unique
class UserRole(StrEnum):
    CLIENT = "client"
    ADMIN = "admin"
