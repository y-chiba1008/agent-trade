from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router
from app.config import validate_startup_settings
from app.db.session import dispose_engine


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    validate_startup_settings()
    yield
    await dispose_engine()


app = FastAPI(
    title='agent-trade',
    lifespan=lifespan,
)
app.include_router(router)
