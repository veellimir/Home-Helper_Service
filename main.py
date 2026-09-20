from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from api.api_v1 import router as api_v1_router
from app.authentication.dependencies.register_access import (
    register_access_rules,
)
from app.authentication.dependencies.rules import ACCESS_RULES
from core.config import settings
from dependecies.functions import init_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_service(app)
    yield


app = FastAPI(
    title="Сервис - Helper Home",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENV != "prod" else None,  # Swagger UI
    redoc_url="/redoc" if settings.ENV != "prod" else None,  # ReDoc
    openapi_url="/openapi.json" if settings.ENV != "prod" else None,
    default_response_class=ORJSONResponse,
)

app.add_middleware(CORSMiddleware, **asdict(settings.cors))
app.include_router(api_v1_router)
register_access_rules(
    routes=app.routes,
    access_rules=ACCESS_RULES,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
