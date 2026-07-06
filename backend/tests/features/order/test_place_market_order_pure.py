from decimal import Decimal

import pytest

from app.features.common.errors import InsufficientBalanceError, ValidationError
from app.features.order.place_market.place_market_order_pure import place_market_order_pure
from app.features.order.shared.order_status import Side


def test_buy_order_updates_balances() -> None:
    result = place_market_order_pure(
        jpy_balance=1_000_000,
        btc_balance=Decimal('0'),
        side=Side.BUY,
        quantity=Decimal('0.01'),
        current_price_jpy=10_000_000,
    )
    assert result.new_jpy_balance == 1_000_000 - 100_000
    assert result.new_btc_balance == Decimal('0.01')
    assert result.execution_price_jpy == 10_000_000
    assert result.trade_cost_jpy == 100_000


def test_sell_order_updates_balances() -> None:
    result = place_market_order_pure(
        jpy_balance=0,
        btc_balance=Decimal('0.01'),
        side=Side.SELL,
        quantity=Decimal('0.01'),
        current_price_jpy=10_000_000,
    )
    assert result.new_jpy_balance == 100_000
    assert result.new_btc_balance == Decimal('0')


def test_insufficient_jpy_balance() -> None:
    with pytest.raises(InsufficientBalanceError):
        place_market_order_pure(
            jpy_balance=1000,
            btc_balance=Decimal('0'),
            side=Side.BUY,
            quantity=Decimal('0.01'),
            current_price_jpy=10_000_000,
        )


def test_insufficient_btc_balance() -> None:
    with pytest.raises(InsufficientBalanceError):
        place_market_order_pure(
            jpy_balance=1_000_000,
            btc_balance=Decimal('0.001'),
            side=Side.SELL,
            quantity=Decimal('0.01'),
            current_price_jpy=10_000_000,
        )


def test_invalid_quantity() -> None:
    with pytest.raises(ValidationError):
        place_market_order_pure(
            jpy_balance=1_000_000,
            btc_balance=Decimal('0'),
            side=Side.BUY,
            quantity=Decimal('0'),
            current_price_jpy=10_000_000,
        )
