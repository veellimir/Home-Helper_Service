from pydantic import EmailStr, Field, computed_field

from app.users.domain.enums import UserRoleEnum
from core.infrastructure.schemas import (
    BaseResponseSchem,
    BaseSchem,
)


class QuestionnaireResponseSchem(BaseResponseSchem):
    first_name: str
    last_name: str
    phone: str | None = None
    address: str | None = None
    age: int | None = None


class UsersListResponseSchem(BaseResponseSchem):
    username: str | None = None


class UserResponseSchem(BaseResponseSchem):
    username: str | None = None
    email: EmailStr | None = None
    role: str = Field(exclude=True)
    questionnaire: QuestionnaireResponseSchem | None = Field(
        default=None, exclude=True
    )

    @computed_field
    def first_name(self) -> str | None:
        return (
            self.questionnaire.first_name
            if self.questionnaire.first_name
            else None
        )

    @computed_field
    def last_name(self) -> str | None:
        return (
            self.questionnaire.last_name
            if self.questionnaire.last_name
            else None
        )

    @computed_field
    def age(self) -> int | None:
        return self.questionnaire.age if self.questionnaire.age else None

    @computed_field
    def phone(self) -> str | None:
        return self.questionnaire.phone if self.questionnaire.phone else None

    @computed_field
    def address(self) -> str | None:
        return (
            self.questionnaire.address if self.questionnaire.address else None
        )


class CreateQuestionnaireSchem(BaseSchem):
    first_name: str
    last_name: str
    phone: str | None = None
    address: str | None = None
    age: int | None = None


class UpdateUserSchem(BaseSchem):
    first_name: str
    last_name: str
    username: str | None = None
    phone: str | None = None
    address: str | None = None
    age: int | None = None


class UserRoleSchem(BaseSchem):
    role: UserRoleEnum
