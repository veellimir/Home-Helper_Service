from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.lessons.infrastructure.models import LessonsORM
from app.lessons.infrastructure.schemes import CreateLessonSchem
from core.infrastructure.dao import SQLAlchemyBaseDAO


class LessonsDAO(SQLAlchemyBaseDAO):
    def __init__(self) -> None:
        self.model = LessonsORM
        super().__init__(LessonsORM)

    async def create_lesson(
        self,
        session: AsyncSession,
        data_lesson: CreateLessonSchem,
    ) -> LessonsORM:
        new_lesson = self.model(
            title=data_lesson.title,
            description=data_lesson.description,
            start_date=data_lesson.start_date,
            end_date=data_lesson.end_date,
        )

        session.add(new_lesson)
        await session.flush()

        return new_lesson

    async def patch_lesson_by_id(
        self,
        session: AsyncSession,
        lesson: LessonsORM,
        data_lesson: dict[str, Any],
    ) -> LessonsORM:
        for field, value in data_lesson.items():
            setattr(lesson, field, value)

        await session.flush()
        return lesson
