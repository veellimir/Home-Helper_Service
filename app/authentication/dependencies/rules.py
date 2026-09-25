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
    ("GET", "/api/v1/users/list"): UserRoleEnum.ADMIN,
    ("GET", "/api/v1/users/current-user"): AccessLevel.AUTHENTICATED,
    ("POST", "/api/v1/users/create"): UserRoleEnum.CLIENT,
    ("PATCH", "/api/v1/users/update"): UserRoleEnum.CLIENT,
    ("PATCH", "/api/v1/users/update-role/{user_id}"): UserRoleEnum.ADMIN,
    ("DELETE", "/api/v1/users/delete"): AccessLevel.AUTHENTICATED,
    # SERVICE
    ("PATCH", "/api/v1/works/{work_id}"): UserRoleEnum.ADMIN,
    ("DELETE", "/api/v1/works/{work_id}"): UserRoleEnum.ADMIN,
    ("POST", "/api/v1/works/create"): UserRoleEnum.ADMIN,
    # BOOKING SERVICE
    ("GET", "/api/v1/work-bookings/list"): AccessLevel.AUTHENTICATED,
    ("GET", "/api/v1/work-bookings/list-detail"): UserRoleEnum.ADMIN,
    ("POST", "/api/v1/work-bookings/create"): UserRoleEnum.CLIENT,
    ("DELETE", "/api/v1/work-bookings/delete"): UserRoleEnum.CLIENT,
}
