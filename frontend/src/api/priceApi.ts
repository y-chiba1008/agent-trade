import { apiRequest } from '@/api/client'
import type { PriceSnapshot } from '@/features/price/shared/priceTypes'

export function getCurrentPrice(): Promise<PriceSnapshot> {
  return apiRequest<PriceSnapshot>('/price/BTC_JPY')
}
