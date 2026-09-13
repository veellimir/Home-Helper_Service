from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.lessons.domain.exceptions import LessonNotFoundException
from app.lessons.infrastructure.dao import LessonsDAO
from app.lessons.infrastructure.models import LessonsORM
from app.lessons.infrastructure.schemes import (
    CreateLessonSchem,
    LessonResponseSchem,
    LessonsListResponseSchem,
    UpdateLessonSchem,
)
from core.domain.service import SQLAlchemyBaseService


class LessonsService(SQLAlchemyBaseService[LessonsORM]):
    def __init__(self, dao: LessonsDAO) -> None:
        self.dao = dao
        super().__init__(self.dao)

    async def get_list_lessons(
        self, session: AsyncSession
    ) -> list[LessonsListResponseSchem]:
        lessons: list[LessonsORM] = await self.dao.get_list_objects(
            session=session
        )
        return [
            LessonsListResponseSchem.model_validate(lesson)
            for lesson in lessons
        ]

    async def get_lesson_by_id(
        self, session: AsyncSession, lesson_id: int
    ) -> LessonResponseSchem | None:
        current_lesson: LessonsORM | None = await self.dao.get_object_by_id(
            session=session, obj_id=lesson_id
        )
        if not current_lesson:
            raise LessonNotFoundException

        return LessonResponseSchem.model_validate(current_lesson)

    async def create_lesson(
        self,
        session: AsyncSession,
        data_lesson: CreateLessonSchem,
    ) -> LessonResponseSchem:
        new_lesson: LessonsORM = await self.dao.create_lesson(
            session=session, data_lesson=data_lesson
        )
        return LessonResponseSchem.model_validate(new_lesson)

    async def patch_lesson_by_id(
        self,
        session: AsyncSession,
        lesson_id: int,
        data_lesson: UpdateLessonSchem,
    ) -> LessonResponseSchem | None:
        current_lesson: LessonsORM | None = await self.dao.get_object_by_id(
            session=session, obj_id=lesson_id
        )
        if not current_lesson:
            raise LessonNotFoundException

        update_lesson: dict[str, Any] = {
            "title": data_lesson.title,
            "description": data_lesson.description,
            "start_date": data_lesson.start_date,
            "end_date": data_lesson.end_date,
        }

        result: LessonsORM = await self.dao.patch_lesson_by_id(
            session=session, lesson=current_lesson, data_lesson=update_lesson
        )
        return LessonResponseSchem.model_validate(result)

    async def delete_lesson_by_id(
        self,
        session: AsyncSession,
        lesson_id: int,
    ):
        pass