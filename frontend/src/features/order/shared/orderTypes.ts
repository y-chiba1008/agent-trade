export type OrderSide = 'buy' | 'sell'

export type Order = {
  id: number
  account_id: number
  order_type: string
  side: OrderSide
  quantity: string
  limit_price: number | null
  status: string
  created_at: string
  updated_at: string
}

export type Execution = {
  id: number
  order_id: number
  quantity: string
  price: number
  executed_at: string
  updated_at: string
}

export type PlaceMarketOrderInput = {
  side: OrderSide
  quantity: string
}

export type PlacedMarketOrderResult = {
  order_id: number
  execution_id: number
  side: OrderSide
  quantity: string
  execution_price_jpy: number
  trade_cost_jpy: number
  new_jpy_balance: number
  new_btc_balance: string
  executed_at: string
}
