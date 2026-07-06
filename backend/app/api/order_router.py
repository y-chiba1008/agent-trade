from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.features.execution.list.list_executions_usecase import list_executions
from app.features.order.list.list_orders_usecase import list_orders
from app.features.order.place_market.place_market_order_usecase import place_market_order
from app.features.order.shared.order_status import Side
from app.features.price.shared.price_source_adapter import PriceSourceAdapter

router = APIRouter(tags=['orders'])


class PlaceMarketOrderRequest(BaseModel):
    side: str
    quantity: Decimal = Field(gt=0)


class OrderResponse(BaseModel):
    id: int
    account_id: int
    order_type: str
    side: str
    quantity: Decimal
    limit_price: int | None
    status: str
    created_at: datetime
    updated_at: datetime


class PlacedMarketOrderResponse(BaseModel):
    order_id: int
    execution_id: int
    side: str
    quantity: Decimal
    execution_price_jpy: int
    trade_cost_jpy: int
    new_jpy_balance: int
    new_btc_balance: Decimal
    executed_at: datetime


class ExecutionResponse(BaseModel):
    id: int
    order_id: int
    quantity: Decimal
    price: int
    executed_at: datetime
    updated_at: datetime


def get_price_adapter(request: Request) -> PriceSourceAdapter:
    return request.app.state.price_adapter


@router.post(
    '/accounts/{account_id}/orders',
    response_model=PlacedMarketOrderResponse,
    status_code=201,
)
async def place_market_order_endpoint(
    account_id: int,
    body: PlaceMarketOrderRequest,
    session: AsyncSession = Depends(get_db_session),
    price_adapter: PriceSourceAdapter = Depends(get_price_adapter),
) -> PlacedMarketOrderResponse:
    if body.side not in (Side.BUY, Side.SELL):
        from app.features.common.errors import ValidationError

        raise ValidationError(f'side は {Side.BUY} または {Side.SELL} である必要があります')

    result = await place_market_order(
        session,
        price_adapter,
        account_id,
        body.side,
        body.quantity,
    )
    return PlacedMarketOrderResponse(
        order_id=result.order_id,
        execution_id=result.execution_id,
        side=result.side,
        quantity=result.quantity,
        execution_price_jpy=result.execution_price_jpy,
        trade_cost_jpy=result.trade_cost_jpy,
        new_jpy_balance=result.new_jpy_balance,
        new_btc_balance=result.new_btc_balance,
        executed_at=result.executed_at,
    )


@router.get('/accounts/{account_id}/orders', response_model=list[OrderResponse])
async def list_orders_endpoint(
    account_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> list[OrderResponse]:
    orders = await list_orders(session, account_id)
    return [
        OrderResponse(
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


@router.get('/accounts/{account_id}/executions', response_model=list[ExecutionResponse])
async def list_executions_endpoint(
    account_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> list[ExecutionResponse]:
    executions = await list_executions(session, account_id)
    return [
        ExecutionResponse(
            id=execution.id,
            order_id=execution.order_id,
            quantity=execution.quantity,
            price=execution.price,
            executed_at=execution.executed_at,
            updated_at=execution.updated_at,
        )
        for execution in executions
    ]
