from dataclasses import dataclass
from decimal import Decimal

from app.features.common.errors import InsufficientBalanceError, ValidationError
from app.features.common.money import calculate_trade_cost_jpy
from app.features.order.shared.order_status import Side


@dataclass(frozen=True)
class MarketOrderResult:
    new_jpy_balance: int
    new_btc_balance: Decimal
    execution_price_jpy: int
    trade_cost_jpy: int


def place_market_order_pure(
    jpy_balance: int,
    btc_balance: Decimal,
    side: str,
    quantity: Decimal,
    current_price_jpy: int,
) -> MarketOrderResult:
    if quantity <= 0:
        raise ValidationError('数量は0より大きい必要があります')
    if side not in (Side.BUY, Side.SELL):
        raise ValidationError(f'side は {Side.BUY} または {Side.SELL} である必要があります')

    trade_cost_jpy = calculate_trade_cost_jpy(quantity, current_price_jpy)

    if side == Side.BUY:
        if jpy_balance < trade_cost_jpy:
            raise InsufficientBalanceError('日本円残高が不足しています')
        return MarketOrderResult(
            new_jpy_balance=jpy_balance - trade_cost_jpy,
            new_btc_balance=btc_balance + quantity,
            execution_price_jpy=current_price_jpy,
            trade_cost_jpy=trade_cost_jpy,
        )

    if btc_balance < quantity:
        raise InsufficientBalanceError('BTC残高が不足しています')
    return MarketOrderResult(
        new_jpy_balance=jpy_balance + trade_cost_jpy,
        new_btc_balance=btc_balance - quantity,
        execution_price_jpy=current_price_jpy,
        trade_cost_jpy=trade_cost_jpy,
    )
