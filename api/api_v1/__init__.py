from fastapi import APIRouter

from core.config import settings

from .auth_router import router as a_router
from .bookings_router import router as b_router
from .users_router import router as u_router
from .works_router import router as w_router
from .notification_sse import router as sse_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(a_router)
router.include_router(u_router)
router.include_router(w_router)
router.include_router(b_router)
router.include_router(sse_router)
