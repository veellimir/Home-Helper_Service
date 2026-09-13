from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.users.infrastructure.models import QuestionnaireORM, UsersORM
from app.users.infrastructure.schemes import (
    CreateQuestionnaireSchem,
)
from core.infrastructure.dao import SQLAlchemyBaseDAO


class UsersDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = UsersORM
        self.questionnaire_model = QuestionnaireORM
        super().__init__(UsersORM)

    async def get_users_list(self, session: AsyncSession) -> list[UsersORM]:
        stmt = select(self.model).order_by(self.model.username)

        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_user_by_id(
        self, session: AsyncSession, user_id: int
    ) -> UsersORM | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.questionnaire))
            .where(self.model.id == user_id)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_questionnaire(
        self,
        session: AsyncSession,
        user_id: int,
        data_questionnaire: CreateQuestionnaireSchem,
    ) -> QuestionnaireORM:
        new_questionnaire = self.questionnaire_model(
            user_id=user_id,
            first_name=data_questionnaire.first_name,
            last_name=data_questionnaire.last_name,
            age=data_questionnaire.age,
        )
        session.add(new_questionnaire)
        await session.flush()

        return new_questionnaire

    async def patch_user_by_id_with_questionnaire(
        self,
        session: AsyncSession,
        current_user: UsersORM,
        user_data: dict[str, object],
        questionnaire_data: dict[str, object],
    ) -> UsersORM:
        for field, value in user_data.items():
            setattr(current_user, field, value)

        if current_user.questionnaire is not None:
            for field, value in questionnaire_data.items():
                setattr(current_user.questionnaire, field, value)

        await session.flush()

        return current_user

    async def delete_user_with_questionnaire(
        self, session: AsyncSession, current_user: UsersORM
    ) -> None:
        await session.delete(current_user)

        if current_user.questionnaire is not None:
            await session.delete(current_user.questionnaire)

        await session.flush()
