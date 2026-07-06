from datetime import datetime

from fastapi import APIRouter, Depends, Request

from app.features.common.errors import PriceUnavailableError
from app.features.price.get_current.get_current_price_usecase import get_current_price
from app.features.price.shared.price_source_adapter import PriceSnapshot, PriceSourceAdapter
from pydantic import BaseModel

router = APIRouter(prefix='/price', tags=['price'])


class PriceResponse(BaseModel):
    product_code: str
    price_jpy: int
    timestamp: datetime


def get_price_adapter(request: Request) -> PriceSourceAdapter:
    return request.app.state.price_adapter


@router.get('/BTC_JPY', response_model=PriceResponse)
async def get_btc_jpy_price(
    price_adapter: PriceSourceAdapter = Depends(get_price_adapter),
) -> PriceResponse:
    snapshot: PriceSnapshot | None = get_current_price(price_adapter, 'BTC_JPY')
    if snapshot is None:
        raise PriceUnavailableError('現在価格を取得できません')
    return PriceResponse(
        product_code=snapshot.product_code,
        price_jpy=snapshot.price_jpy,
        timestamp=snapshot.timestamp,
    )
