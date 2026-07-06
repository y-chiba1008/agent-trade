from app.features.price.shared.price_source_adapter import PriceSnapshot, PriceSourceAdapter


def get_current_price(
    price_adapter: PriceSourceAdapter,
    product_code: str,
) -> PriceSnapshot | None:
    return price_adapter.get_current_price(product_code)
