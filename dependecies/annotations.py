from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.service import UsersService
from app.works.domain.service import WorksService
from core.database import get_async_session
from dependecies.functions import get_users_service, get_works_service

DBSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
WorksServiceDep = Annotated[WorksService, Depends(get_works_service)]
