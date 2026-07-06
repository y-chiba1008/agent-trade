import { useQuery } from '@tanstack/react-query'
import { getCurrentPrice } from '@/api/priceApi'
import type { PriceSnapshot } from '@/features/price/shared/priceTypes'

export const PRICE_QUERY_KEY = ['price', 'BTC_JPY'] as const
const PRICE_REFETCH_INTERVAL_MS = 2000

// 将来 WebSocket 化する際は、この fetcher を差し替える
async function fetchPriceSnapshot(): Promise<PriceSnapshot> {
  return getCurrentPrice()
}

export function usePriceQuery() {
  return useQuery({
    queryKey: PRICE_QUERY_KEY,
    queryFn: fetchPriceSnapshot,
    refetchInterval: PRICE_REFETCH_INTERVAL_MS,
  })
}
