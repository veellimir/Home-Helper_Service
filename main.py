from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api_v1 import router as api_v1_router
from core.config import settings
from dependecies.functions import init_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_service(app)
    yield


app = FastAPI(
    title="Сервис - Спортивный Клуб",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENV != "prod" else None,  # Swagger UI
    redoc_url="/redoc" if settings.ENV != "prod" else None,  # ReDoc
    openapi_url="/openapi.json" if settings.ENV != "prod" else None,
)

app.add_middleware(CORSMiddleware, **asdict(settings.cors))
app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
