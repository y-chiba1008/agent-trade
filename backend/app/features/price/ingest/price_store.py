from app.features.price.shared.price_source_adapter import PriceSnapshot


class PriceStore:
    """プロセス内で最新価格を保持するシングルトンストア。"""

    def __init__(self) -> None:
        self._prices: dict[str, PriceSnapshot] = {}

    def update(self, snapshot: PriceSnapshot) -> None:
        self._prices[snapshot.product_code] = snapshot

    def get(self, product_code: str) -> PriceSnapshot | None:
        return self._prices.get(product_code)


_price_store: PriceStore | None = None


def get_price_store() -> PriceStore:
    global _price_store
    if _price_store is None:
        _price_store = PriceStore()
    return _price_store
