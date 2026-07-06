import { useMutation, useQueryClient } from '@tanstack/react-query'
import { placeMarketOrder } from '@/api/orderApi'
import { ACCOUNTS_QUERY_KEY } from '@/features/account/list/useAccountsQuery'
import { executionsQueryKey } from '@/features/execution/list/useExecutionsQuery'
import { ordersQueryKey } from '@/features/order/list/useOrdersQuery'
import type { PlaceMarketOrderInput } from '@/features/order/shared/orderTypes'

type PlaceMarketOrderVariables = {
  accountId: number
  input: PlaceMarketOrderInput
}

export function usePlaceMarketOrderMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ accountId, input }: PlaceMarketOrderVariables) =>
      placeMarketOrder(accountId, input),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: ACCOUNTS_QUERY_KEY })
      void queryClient.invalidateQueries({
        queryKey: ordersQueryKey(variables.accountId),
      })
      void queryClient.invalidateQueries({
        queryKey: executionsQueryKey(variables.accountId),
      })
    },
  })
}
