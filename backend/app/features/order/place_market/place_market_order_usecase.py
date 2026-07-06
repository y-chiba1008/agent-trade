from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.order.place_market.place_market_order_io import (
    PlacedMarketOrderResult,
    place_market_order as place_market_order_io,
)
from app.features.price.shared.price_source_adapter import PriceSourceAdapter


async def place_market_order(
    session: AsyncSession,
    price_adapter: PriceSourceAdapter,
    account_id: int,
    side: str,
    quantity: Decimal,
) -> PlacedMarketOrderResult:
    return await place_market_order_io(session, price_adapter, account_id, side, quantity)
