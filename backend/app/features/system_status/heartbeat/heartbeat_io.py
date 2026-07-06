import asyncio
import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.system_status_model import SystemStatusModel
from app.db.session import get_session_factory

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL_SEC = 30


async def upsert_heartbeat(session: AsyncSession) -> None:
    now = datetime.now(UTC)
    result = await session.execute(select(SystemStatusModel).limit(1))
    row = result.scalar_one_or_none()
    if row is None:
        session.add(SystemStatusModel(last_heartbeat_at=now))
    else:
        row.last_heartbeat_at = now
    await session.commit()


async def heartbeat_loop(stop_event: asyncio.Event) -> None:
    session_factory = get_session_factory()
    while not stop_event.is_set():
        try:
            async with session_factory() as session:
                await upsert_heartbeat(session)
        except Exception:
            logger.exception('ハートビート更新に失敗しました')
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=HEARTBEAT_INTERVAL_SEC)
        except TimeoutError:
            continue


def start_heartbeat() -> tuple[asyncio.Task[None], asyncio.Event]:
    stop_event = asyncio.Event()
    task = asyncio.create_task(heartbeat_loop(stop_event))
    return task, stop_event
