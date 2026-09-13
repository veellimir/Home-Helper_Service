from app.users.infrastructure.models import UsersORM
from core.infrastructure.dao import SQLAlchemyBaseDAO


class AuthDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = UsersORM
        super().__init__(UsersORM)
