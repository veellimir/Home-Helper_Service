from enum import StrEnum, unique


@unique
class UserRoleEnum(StrEnum):
    CLIENT = "client"
    ADMIN = "admin"
