from sqlalchemy.ext.asyncio import AsyncSession

from app.features.order.list.list_orders_io import OrderData, list_orders as list_orders_io


async def list_orders(session: AsyncSession, account_id: int) -> list[OrderData]:
    return await list_orders_io(session, account_id)
