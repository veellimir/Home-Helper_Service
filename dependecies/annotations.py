from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lessons.domain.service import LessonsService
from app.users.domain.service import UsersService
from core.database import get_async_session
from dependecies.functions import get_lessons_service, get_users_service

DBSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
LessonServiceDep = Annotated[LessonsService, Depends(get_lessons_service)]
