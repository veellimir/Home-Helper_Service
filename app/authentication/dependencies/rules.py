from app.authentication.domain.enums import AccessLevel
from app.users.domain.enums import UserRoleEnum

ACCESS_RULES: dict[tuple[str, str], UserRoleEnum | AccessLevel] = {
    ("POST", "/api/v1/auth/logout"): AccessLevel.AUTHENTICATED,
    ("GET", "/api/v1/users/list"): UserRoleEnum.ADMIN,
}
