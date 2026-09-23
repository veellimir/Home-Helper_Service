from app.authentication.domain.enums import AccessLevel
from app.users.domain.enums import UserRoleEnum

# ОПИСАНИЯ ПРАВИЛ ДЛЯ МАРШРУТОВ
ACCESS_RULES: dict[tuple[str, str], UserRoleEnum | AccessLevel] = {
    # AUTH
    ("POST", "/api/v1/auth/refresh"): AccessLevel.AUTHENTICATED,
    ("POST", "/api/v1/auth/forgot-password"): AccessLevel.AUTHENTICATED,
    ("POST", "/api/v1/auth/reset-password"): AccessLevel.AUTHENTICATED,
    ("POST", "/api/v1/auth/logout"): AccessLevel.AUTHENTICATED,

    # USERS
    ("GET", "/api/v1/users/{user_id}"): AccessLevel.AUTHENTICATED,
    ("GET", "/api/v1/users/list"): UserRoleEnum.ADMIN,
    ("POST", "/api/v1/users/{user_id}"): UserRoleEnum.CLIENT,
    ("PATCH", "/api/v1/users/{user_id}"): UserRoleEnum.CLIENT,
    ("PATCH", "/api/v1/users/update-role/{user_id}"): UserRoleEnum.ADMIN,
    ("DELETE", "/api/v1/users/{user_id}"): AccessLevel.AUTHENTICATED,

    # SERVICE
    ("PATCH", "/api/v1/works/{work_id}"): UserRoleEnum.ADMIN,
    ("DELETE", "/api/v1/works/{work_id}"): UserRoleEnum.ADMIN,
    ("POST", "/api/v1/works/crete"): UserRoleEnum.ADMIN,

    # BOOKING SERVICE
    ("POST", "/api/v1/work-booking/crete"): UserRoleEnum.CLIENT,
}
