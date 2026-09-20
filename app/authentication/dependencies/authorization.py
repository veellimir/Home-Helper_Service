from collections.abc import Callable
from typing import Any

from app.authentication.dependencies.current_user import CurrentUserDep
from app.authentication.domain.enums import AccessLevel
from app.authentication.domain.exceptions import UnauthorizedNotFoundException
from app.users.domain.enums import UserRoleEnum
from app.users.infrastructure.schemes import UserResponseSchem


def require_role(
    required_role: UserRoleEnum | AccessLevel,
) -> Callable[..., Any]:

    async def role_checker(
        current_user: CurrentUserDep,
    ) -> UserResponseSchem:
        if required_role == AccessLevel.AUTHENTICATED:
            return current_user

        if current_user.role != required_role:
            raise UnauthorizedNotFoundException

        return current_user

    return role_checker
