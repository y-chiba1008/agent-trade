from decimal import Decimal

import pytest

from app.db.session import get_session_factory
from app.features.account.create.create_account_usecase import create_account
from app.features.order.place_market.place_market_order_usecase import place_market_order
from tests.fake_price_adapter import FakePriceSourceAdapter


@pytest.mark.asyncio
async def test_place_market_buy_order() -> None:
    price_adapter = FakePriceSourceAdapter(price_jpy=10_000_000)
    session_factory = get_session_factory()
    async with session_factory() as session:
        account = await create_account(
            session,
            name='trade-test',
            account_tag='human',
            initial_jpy_balance=1_000_000,
        )
        result = await place_market_order(
            session,
            price_adapter,
            account.id,
            'buy',
            Decimal('0.001'),
        )
        assert result.execution_price_jpy == 10_000_000
        assert result.trade_cost_jpy == 10_000
        assert result.new_jpy_balance == 990_000
        assert result.new_btc_balance == Decimal('0.001')
