from app.authentication.domain.enums import AccessLevel
from app.users.domain.enums import UserRoleEnum

ACCESS_RULES: dict[tuple[str, str], UserRoleEnum | AccessLevel] = {
    # AUTH
    ("POST", "/api/v1/auth/logout"): AccessLevel.AUTHENTICATED,

    # USERS
    ("GET", "/api/v1/users/{user_id}"): AccessLevel.AUTHENTICATED,
    ("GET", "/api/v1/users/list"): UserRoleEnum.ADMIN,
    ("POST", "/api/v1/users/{user_id}"): UserRoleEnum.CLIENT,
    ("PATCH", "/api/v1/users/{user_id}"): UserRoleEnum.CLIENT,
    ("PATCH", "/api/v1/users/update-role/{user_id}"): UserRoleEnum.ADMIN,
    ("DELETE", "/api/v1/users/{user_id}"): AccessLevel.AUTHENTICATED,

    # SERVICE

    # BOOKING SERVICE
}
