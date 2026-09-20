from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.authentication.infrastructure.security import TokenService
from app.users.domain.exceptions import UserNotFoundException
from app.users.infrastructure.dao import UsersDAO
from app.users.infrastructure.schemes import UserResponseSchem
from dependecies.annotations import DBSessionDep

bearer_scheme = HTTPBearer()


BearerCredentialsDep = Annotated[
    HTTPAuthorizationCredentials,
    Depends(bearer_scheme),
]


async def get_current_user(
    credentials: BearerCredentialsDep,
    session: DBSessionDep,
) -> UserResponseSchem:
    user_id = TokenService.get_user_id_from_access_token(
        credentials.credentials,
    )

    users_dao = UsersDAO()

    user = await users_dao.get_user_by_id(
        session=session,
        user_id=user_id,
    )

    if user is None:
        raise UserNotFoundException

    return UserResponseSchem.model_validate(user)


CurrentUserDep = Annotated[
    UserResponseSchem,
    Depends(get_current_user),
]
