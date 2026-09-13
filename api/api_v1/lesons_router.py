from fastapi import APIRouter

from app.lessons.infrastructure.schemes import (
    CreateLessonSchem,
    LessonResponseSchem,
    LessonsListResponseSchem,
    UpdateLessonSchem,
)
from core.config import settings
from dependecies.annotations import (
    DBSessionDep,
    LessonServiceDep,
)

router = APIRouter(prefix=settings.api.v1.lessons, tags=["Занятия клуба"])


@router.get("/list", summary="Получить список занятий")
async def get_list_lessons(
    session: DBSessionDep, service: LessonServiceDep
) -> list[LessonsListResponseSchem]:
    return await service.get_list_lessons(session=session)


@router.get("/{lesson_id}", summary="Получить занятие по ID")
async def get_lesson_by_id(
    session: DBSessionDep, service: LessonServiceDep, lesson_id: int
) -> LessonResponseSchem | None:
    return await service.get_lesson_by_id(
        session=session, lesson_id=lesson_id
    )


@router.post("/create", summary="Создание занятия")
async def create_lesson(
    session: DBSessionDep,
    service: LessonServiceDep,
    data: CreateLessonSchem,
) -> LessonResponseSchem:
    return await service.create_lesson(session=session, data_lesson=data)


@router.patch("/{lesson_id}", summary="Обновить занятие по ID")
async def patch_lesson_by_id(
    session: DBSessionDep,
    service: LessonServiceDep,
    lesson_id: int,
    data: UpdateLessonSchem,
) -> LessonResponseSchem | None:
    return await service.patch_lesson_by_id(
        session=session, lesson_id=lesson_id, data_lesson=data
    )


@router.delete("/{lesson_id}", summary="Удаление занятие")
async def delete_lesson_by_id(
    session: DBSessionDep,
    service: LessonServiceDep,
    lesson_id: int,
):
    return await service.delete_lesson_by_id(
        session=session,
        lesson_id=lesson_id
    )