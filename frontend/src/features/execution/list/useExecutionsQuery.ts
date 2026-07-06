import { useQuery } from '@tanstack/react-query'
import { listExecutions } from '@/api/orderApi'

export const executionsQueryKey = (accountId: number) =>
  ['executions', accountId] as const

export function useExecutionsQuery(accountId: number) {
  return useQuery({
    queryKey: executionsQueryKey(accountId),
    queryFn: () => listExecutions(accountId),
    enabled: accountId > 0,
  })
}
