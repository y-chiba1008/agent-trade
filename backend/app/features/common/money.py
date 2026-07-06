from decimal import Decimal, ROUND_HALF_UP


def ltp_to_jpy(ltp: float) -> int:
    """bitFlyer ltp（float）を円単位の整数に変換する。"""
    return int(Decimal(str(ltp)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def calculate_trade_cost_jpy(quantity: Decimal, price_jpy: int) -> int:
    """BTC数量と価格（円）から取引金額（円）を計算する。切り上げで整数円化。"""
    cost = quantity * Decimal(price_jpy)
    return int(cost.to_integral_value(rounding=ROUND_HALF_UP))
