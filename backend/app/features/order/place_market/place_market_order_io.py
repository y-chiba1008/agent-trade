from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.account_model import AccountModel
from app.db.models.execution_model import ExecutionModel
from app.db.models.order_model import OrderModel
from app.features.common.errors import NotFoundError, PriceUnavailableError
from app.features.order.place_market.place_market_order_pure import (
    MarketOrderResult,
    place_market_order_pure,
)
from app.features.order.shared.order_status import OrderStatus, OrderType
from app.features.price.shared.price_source_adapter import PriceSourceAdapter


@dataclass(frozen=True)
class PlacedMarketOrderResult:
    order_id: int
    execution_id: int
    side: str
    quantity: Decimal
    execution_price_jpy: int
    trade_cost_jpy: int
    new_jpy_balance: int
    new_btc_balance: Decimal
    executed_at: datetime


async def place_market_order(
    session: AsyncSession,
    price_adapter: PriceSourceAdapter,
    account_id: int,
    side: str,
    quantity: Decimal,
) -> PlacedMarketOrderResult:
    price_snapshot = price_adapter.get_current_price('BTC_JPY')
    if price_snapshot is None:
        raise PriceUnavailableError('現在価格を取得できません')

    result = await session.execute(
        select(AccountModel).where(AccountModel.id == account_id).with_for_update()
    )
    account = result.scalar_one_or_none()
    if account is None:
        raise NotFoundError(f'口座 id={account_id} が見つかりません')

    order_result: MarketOrderResult = place_market_order_pure(
        jpy_balance=account.jpy_balance,
        btc_balance=account.btc_balance,
        side=side,
        quantity=quantity,
        current_price_jpy=price_snapshot.price_jpy,
    )

    now = datetime.now(UTC)
    order = OrderModel(
        account_id=account_id,
        order_type=OrderType.MARKET,
        side=side,
        quantity=quantity,
        limit_price=None,
        status=OrderStatus.FILLED,
        updated_at=now,
    )
    session.add(order)
    await session.flush()

    execution = ExecutionModel(
        order_id=order.id,
        quantity=quantity,
        price=order_result.execution_price_jpy,
        executed_at=now,
        updated_at=now,
    )
    session.add(execution)

    account.jpy_balance = order_result.new_jpy_balance
    account.btc_balance = order_result.new_btc_balance
    account.updated_at = now

    await session.commit()
    await session.refresh(order)
    await session.refresh(execution)

    return PlacedMarketOrderResult(
        order_id=order.id,
        execution_id=execution.id,
        side=side,
        quantity=quantity,
        execution_price_jpy=order_result.execution_price_jpy,
        trade_cost_jpy=order_result.trade_cost_jpy,
        new_jpy_balance=order_result.new_jpy_balance,
        new_btc_balance=order_result.new_btc_balance,
        executed_at=execution.executed_at,
    )
