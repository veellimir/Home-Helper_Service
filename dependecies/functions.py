from fastapi import FastAPI, Request

from app.users.domain.service import UsersService
from app.users.infrastructure.dao import UsersDAO
from app.works.domain.service import WorksService
from app.works.infrastructure.dao import WorksDAO


def init_service(app: FastAPI) -> None:
    # DAO
    users_dao = UsersDAO()
    works_dao = WorksDAO()

    # Services
    users_service = UsersService(users_dao)
    works_service = WorksService(works_dao)

    # State
    app.state.user_service = users_service
    app.state.works_service = works_service


def get_users_service(request: Request) -> UsersService:
    return request.app.state.user_service


def get_works_service(request: Request) -> WorksService:
    return request.app.state.works_service
