from fastapi import APIRouter

from app.users.infrastructure.schemes import (
    CreateQuestionnaireSchem,
    UpdateUserSchem,
    UserResponseSchem,
    UserRoleSchem,
    UsersListResponseSchem,
)
from core.config import settings
from dependecies.annotations import (
    DBSessionDep,
    UsersServiceDep,
)

router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])


@router.get("/list", summary="Получить список пользователей")
async def get_users_list(
    session: DBSessionDep,
    service: UsersServiceDep,
) -> list[UsersListResponseSchem]:
    """
    Возвращает список пользователей

    :params: None
    """
    return await service.get_users_list(session=session)


@router.get("/{user_id}", summary="Получить пользователя по ID")
async def get_user_by_id(
    session: DBSessionDep,
    service: UsersServiceDep,
    user_id: int,
) -> UserResponseSchem | None:
    """
    Возвращает подробную информацию по текущему пользователю

    :user_id идентификатор пользователя
    """
    return await service.get_user_by_id(session=session, user_id=user_id)


@router.post("/{user_id}", summary="Создание анкеты")
async def create_questionnaire(
    session: DBSessionDep,
    service: UsersServiceDep,
    user_id: int,
    data: CreateQuestionnaireSchem,
) -> UserResponseSchem | None:
    """
    Создает анкету для текущего пользователя

    :user_id Идентификатор текущего пользователя \n
    :first_name Имя пользователя \n
    :last_name Фамилия пользователя \n
    :age Возраст
    """
    return await service.create_questionnaire(
        session=session, user_id=user_id, data_questionnaire=data
    )


@router.patch(
    "/update-role/{user_id}", summary="Изменить роль пользователю по ID"
)
async def patch_role_user_by_id(
    session: DBSessionDep,
    service: UsersServiceDep,
    user_id: int,
    data_role: UserRoleSchem,
) -> UserRoleSchem:
    """
    Редактирует роль пользователя

    :user_id Идентификатор текущего пользователя \n
    :return: str Обновлённая роль
    """
    return await service.patch_role_user_by_id(
        session=session, user_id=user_id, update_role=data_role.role
    )


@router.patch("/{user_id}", summary="Обновление анкеты")
async def patch_user_with_questionnaire(
    session: DBSessionDep,
    service: UsersServiceDep,
    user_id: int,
    data: UpdateUserSchem,
) -> UserResponseSchem | None:
    """
    Редактирует анкету текущего пользователя

    :user_id идентификатор пользователя \n
    :first_name Имя пользователя \n
    :last_name Фамилия пользователя \n
    :age Возраст
    """
    return await service.patch_user_by_id_with_questionnaire(
        session=session, user_id=user_id, data_questionnaire=data
    )


@router.delete("/{user_id}", summary="Удаление пользователя и анкеты")
async def delete_user_with_questionnaire(
    session: DBSessionDep,
    service: UsersServiceDep,
    user_id: int,
) -> None:
    """
    Удаляет анкету текущего пользователя

    :user_id идентификатор пользователя
    """
    await service.delete_user_with_questionnaire(
        session=session, user_id=user_id
    )
