import { apiRequest } from '@/api/client'
import type {
  Execution,
  Order,
  PlaceMarketOrderInput,
  PlacedMarketOrderResult,
} from '@/features/order/shared/orderTypes'

export function placeMarketOrder(
  accountId: number,
  input: PlaceMarketOrderInput,
): Promise<PlacedMarketOrderResult> {
  return apiRequest<PlacedMarketOrderResult>(`/accounts/${accountId}/orders`, {
    method: 'POST',
    body: input,
  })
}

export function listOrders(accountId: number): Promise<Order[]> {
  return apiRequest<Order[]>(`/accounts/${accountId}/orders`)
}

export function listExecutions(accountId: number): Promise<Execution[]> {
  return apiRequest<Execution[]>(`/accounts/${accountId}/executions`)
}
