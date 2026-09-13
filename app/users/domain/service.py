from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.exceptions import (
    QuestionnaireConflictException,
    UserNotFoundException,
)
from app.users.infrastructure.dao import UsersDAO
from app.users.infrastructure.models import QuestionnaireORM, UsersORM
from app.users.infrastructure.schemes import (
    CreateQuestionnaireSchem,
    UpdateUserSchem,
    UserResponseSchem,
    UsersListResponseSchem,
)
from core.domain.service import SQLAlchemyBaseService


class UsersService(SQLAlchemyBaseService[UsersORM]):
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao
        super().__init__(self.dao)

    async def get_users_list(
        self, session: AsyncSession
    ) -> list[UsersListResponseSchem]:
        users: list[UsersORM] = await self.dao.get_users_list(session=session)

        return [UsersListResponseSchem.model_validate(user) for user in users]

    async def get_user_by_id(
        self, session: AsyncSession, user_id: int
    ) -> UserResponseSchem | None:
        current_user: (
            UserResponseSchem | None
        ) = await self.dao.get_user_by_id(session=session, user_id=user_id)
        if not current_user:
            raise UserNotFoundException

        return UserResponseSchem.model_validate(current_user)

    async def create_questionnaire(
        self,
        session: AsyncSession,
        user_id: int,
        data_questionnaire: CreateQuestionnaireSchem,
    ) -> UserResponseSchem | None:
        current_user: UserResponseSchem | None = await self.get_user_by_id(
            session=session, user_id=user_id
        )

        if current_user.questionnaire:
            raise QuestionnaireConflictException

        new_questionnaire: QuestionnaireORM = (
            await self.dao.create_questionnaire(
                session=session,
                user_id=user_id,
                data_questionnaire=data_questionnaire,
            )
        )
        current_user.questionnaire = new_questionnaire

        return UserResponseSchem.model_validate(current_user)

    async def patch_user_by_id_with_questionnaire(
        self,
        session: AsyncSession,
        user_id: int,
        data_questionnaire: UpdateUserSchem,
    ) -> UserResponseSchem | None:
        current_user: UsersORM | None = await self.dao.get_user_by_id(
            session=session, user_id=user_id
        )
        if not current_user:
            raise UserNotFoundException

        update_data: dict[str, Any] = data_questionnaire.model_dump(
            exclude_unset=True
        )
        user_fields: set[str] = {"username"}
        questionnaire_fields: set[str] = {"first_name", "last_name", "age"}

        user_data: dict[str, str] = {
            field: value
            for field, value in update_data.items()
            if field in user_fields
        }

        questionnaire_data: dict[str, Any] = {
            field: value
            for field, value in update_data.items()
            if field in questionnaire_fields
        }

        await self.dao.patch_user_by_id_with_questionnaire(
            session=session,
            current_user=current_user,
            user_data=user_data,
            questionnaire_data=questionnaire_data,
        )

        return UserResponseSchem.model_validate(current_user)

    async def delete_user_with_questionnaire(
        self, session: AsyncSession, user_id: int
    ) -> None:
        current_user: UsersORM | None = await self.dao.get_user_by_id(
            session=session, user_id=user_id
        )
        if not current_user:
            raise UserNotFoundException

        await self.dao.delete_user_with_questionnaire(
            session=session, current_user=current_user
        )
