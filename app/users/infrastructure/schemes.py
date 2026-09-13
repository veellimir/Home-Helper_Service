from pydantic import Field, computed_field

from core.infrastructure.schemas import (
    BaseResponseSchem,
    BaseSchem,
)


class QuestionnaireResponseSchem(BaseSchem):
    first_name: str
    last_name: str
    age: int | None = None


class UsersListResponseSchem(BaseResponseSchem):
    username: str


class UserResponseSchem(BaseResponseSchem):
    username: str
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
