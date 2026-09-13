from fastapi import FastAPI, Request

from app.lessons.domain.service import LessonsService
from app.lessons.infrastructure.dao import LessonsDAO
from app.users.domain.service import UsersService
from app.users.infrastructure.dao import UsersDAO


def init_service(app: FastAPI) -> None:
    # DAO
    users_dao = UsersDAO()
    lessons_dao = LessonsDAO()

    # Services
    users_service = UsersService(users_dao)
    lessons_service = LessonsService(lessons_dao)

    # State
    app.state.user_service = users_service
    app.state.lessons_service = lessons_service


def get_users_service(request: Request) -> UsersService:
    return request.app.state.user_service


def get_lessons_service(request: Request) -> LessonsService:
    return request.app.state.lessons_service
