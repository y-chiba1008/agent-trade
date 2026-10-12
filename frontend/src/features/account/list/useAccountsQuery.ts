import { useQuery } from '@tanstack/react-query'
import { listAccounts } from '@/api/accountApi'

export const ACCOUNTS_QUERY_KEY = ['accounts'] as const

export function useAccountsQuery() {
  return useQuery({
    queryKey: ACCOUNTS_QUERY_KEY,
    queryFn: listAccounts,
  })
}
