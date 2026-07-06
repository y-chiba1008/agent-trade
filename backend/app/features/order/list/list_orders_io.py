from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order_model import OrderModel
from app.features.common.errors import NotFoundError
from app.db.models.account_model import AccountModel


@dataclass(frozen=True)
class OrderData:
    id: int
    account_id: int
    order_type: str
    side: str
    quantity: Decimal
    limit_price: int | None
    status: str
    created_at: datetime
    updated_at: datetime


async def list_orders(session: AsyncSession, account_id: int) -> list[OrderData]:
    account_exists = await session.execute(
        select(AccountModel.id).where(AccountModel.id == account_id)
    )
    if account_exists.scalar_one_or_none() is None:
        raise NotFoundError(f'口座 id={account_id} が見つかりません')

    result = await session.execute(
        select(OrderModel)
        .where(OrderModel.account_id == account_id)
        .order_by(OrderModel.id.desc())
    )
    orders = result.scalars().all()
    return [
        OrderData(
            id=order.id,
            account_id=order.account_id,
            order_type=order.order_type,
            side=order.side,
            quantity=order.quantity,
            limit_price=order.limit_price,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        for order in orders
    ]
