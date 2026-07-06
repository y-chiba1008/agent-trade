import { useQuery } from '@tanstack/react-query'
import { listOrders } from '@/api/orderApi'

export const ordersQueryKey = (accountId: number) => ['orders', accountId] as const

export function useOrdersQuery(accountId: number) {
  return useQuery({
    queryKey: ordersQueryKey(accountId),
    queryFn: () => listOrders(accountId),
    enabled: accountId > 0,
  })
}
