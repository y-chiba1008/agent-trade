from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exceptions import register_exception_handlers
from app.api.router import router
from app.config import validate_startup_settings
from app.db.session import dispose_engine
from app.features.price.ingest.bitflyer_realtime_io import BitflyerRealtimeAdapter
from app.features.price.ingest.price_store import get_price_store
from app.features.system_status.heartbeat.heartbeat_usecase import start_heartbeat


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    validate_startup_settings()

    price_store = get_price_store()
    price_adapter = BitflyerRealtimeAdapter(price_store)
    await price_adapter.start()
    app.state.price_adapter = price_adapter

    heartbeat_task, heartbeat_stop_event = start_heartbeat()

    yield

    heartbeat_stop_event.set()
    heartbeat_task.cancel()
    try:
        await heartbeat_task
    except Exception:
        pass

    await price_adapter.stop()
    await dispose_engine()


app = FastAPI(
    title='agent-trade',
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
)
register_exception_handlers(app)
app.include_router(router)
