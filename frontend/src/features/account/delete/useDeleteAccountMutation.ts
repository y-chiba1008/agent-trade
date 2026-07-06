import { useMutation, useQueryClient } from '@tanstack/react-query'
import { deleteAccount } from '@/api/accountApi'
import { ACCOUNTS_QUERY_KEY } from '@/features/account/list/useAccountsQuery'

export function useDeleteAccountMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (accountId: number) => deleteAccount(accountId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ACCOUNTS_QUERY_KEY })
    },
  })
}
