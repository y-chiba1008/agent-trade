from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class PriceSnapshot:
    product_code: str
    price_jpy: int
    timestamp: datetime


class PriceSourceAdapter(Protocol):
    async def start(self) -> None: ...

    async def stop(self) -> None: ...

    def get_current_price(self, product_code: str) -> PriceSnapshot | None: ...
