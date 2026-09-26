from fastapi import FastAPI, Request

from app.authentication.domain.service import AuthService
from app.authentication.infrastructure.dao import AuthDAO
from app.bookings.domain.service import WorkBookingService
from app.bookings.infrastructure.dao import WorkBookingDAO
from app.sse.manager import sse_manager
from app.sse.publisher import EventPublisher
from app.users.domain.service import UsersService
from app.users.infrastructure.dao import UsersDAO
from app.works.domain.service import WorksService
from app.works.infrastructure.dao import WorksDAO


def init_service(app: FastAPI) -> None:
    # DAO
    auth_dao = AuthDAO()
    users_dao = UsersDAO()
    works_dao = WorksDAO()
    work_booking_dao = WorkBookingDAO()

    # Notifications
    event_publisher = EventPublisher(
        sse_manager=sse_manager,
    )

    # Services
    auth_service = AuthService(auth_dao)
    users_service = UsersService(users_dao)
    works_service = WorksService(works_dao)
    work_booking_service = WorkBookingService(
        dao=work_booking_dao,
        works_service=works_service,
        users_service=users_service,
        event_publisher=event_publisher,
    )

    # State
    app.state.auth_service = auth_service
    app.state.user_service = users_service
    app.state.works_service = works_service
    app.state.work_booking_service = work_booking_service


def get_auth_service(request: Request) -> AuthService:
    return request.app.state.auth_service


def get_users_service(request: Request) -> UsersService:
    return request.app.state.user_service


def get_works_service(request: Request) -> WorksService:
    return request.app.state.works_service


def get_work_bookings_service(request: Request) -> WorkBookingService:
    return request.app.state.work_booking_service
