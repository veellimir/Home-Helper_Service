from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.infrastructure.dao import AuthDAO
from app.authentication.infrastructure.schemes import RegisterUserSchem
from app.users.domain.exceptions import (
    UserConflictException,
    UsernameEmailNotNullException,
)
from app.users.infrastructure.dao import UsersDAO
from app.users.infrastructure.models import UsersORM
from core.domain.service import SQLAlchemyBaseService


class AuthService(SQLAlchemyBaseService[UsersORM]):
    def __init__(self, dao: AuthDAO) -> None:
        self.dao = dao
        self.user_dao = UsersDAO()
        super().__init__(self.dao)

    async def register_user(
        self, session: AsyncSession, user_data: RegisterUserSchem
    ) -> None:
        if not user_data.username and not user_data.email:
            raise UsernameEmailNotNullException

        current_username: bool = False
        current_email: bool = False

        if user_data.username:
            current_username: bool = await self.user_dao.get_by_username(
                session=session, username=user_data.username
            )
        if user_data.email:
            current_email: bool = await self.user_dao.get_by_email(
                session=session, email=user_data.email
            )

        if current_username or current_email:
            raise UserConflictException

        await self.user_dao.create_user(session=session, user_data=user_data)
