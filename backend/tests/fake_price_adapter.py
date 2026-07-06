from datetime import UTC, datetime

from app.features.price.shared.price_source_adapter import PriceSnapshot


class FakePriceSourceAdapter:
    def __init__(self, price_jpy: int = 10_000_000) -> None:
        self._price_jpy = price_jpy
        self._started = False

    async def start(self) -> None:
        self._started = True

    async def stop(self) -> None:
        self._started = False

    def set_price(self, price_jpy: int) -> None:
        self._price_jpy = price_jpy

    def get_current_price(self, product_code: str) -> PriceSnapshot | None:
        if product_code != 'BTC_JPY':
            return None
        return PriceSnapshot(
            product_code=product_code,
            price_jpy=self._price_jpy,
            timestamp=datetime.now(UTC),
        )
