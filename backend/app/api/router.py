from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.account_router import router as account_router
from app.api.order_router import router as order_router
from app.api.price_router import router as price_router
from app.db.health_io import check_db_connection
from app.db.session import get_db_session

router = APIRouter()


@router.get('/health')
async def health_check(
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    db_connected = await check_db_connection(session)
    if not db_connected:
        response.status_code = 503
        return {'status': 'degraded', 'db': 'disconnected'}
    return {'status': 'ok', 'db': 'connected'}


router.include_router(account_router)
router.include_router(order_router)
router.include_router(price_router)
