from pydantic import EmailStr, Field, computed_field

from app.users.domain.enums import UserRoleEnum
from core.infrastructure.schemas import (
    BaseResponseSchem,
    BaseSchem,
)


class QuestionnaireResponseSchem(BaseResponseSchem):
    first_name: str
    last_name: str
    age: int | None = None


class UsersListResponseSchem(BaseResponseSchem):
    username: str | None = None


class UserResponseSchem(BaseResponseSchem):
    username: str | None = None
    email: EmailStr | None = None
    role: UserRoleEnum
    questionnaire: QuestionnaireResponseSchem | None = Field(
        default=None, exclude=True
    )

    @computed_field
    def first_name(self) -> str | None:
        return self.questionnaire.first_name if self.questionnaire else None

    @computed_field
    def last_name(self) -> str | None:
        return self.questionnaire.last_name if self.questionnaire else None

    @computed_field
    def age(self) -> int | None:
        return self.questionnaire.age if self.questionnaire else None


class CreateQuestionnaireSchem(QuestionnaireResponseSchem):
    pass


class UpdateUserSchem(QuestionnaireResponseSchem):
    username: str


class UserRoleSchem(BaseSchem):
    role: UserRoleEnum
