import { useMutation, useQueryClient } from '@tanstack/react-query'
import { createAccount } from '@/api/accountApi'
import { ACCOUNTS_QUERY_KEY } from '@/features/account/list/useAccountsQuery'
import type { CreateAccountInput } from '@/features/account/shared/accountTypes'

export function useCreateAccountMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (input: CreateAccountInput) => createAccount(input),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ACCOUNTS_QUERY_KEY })
    },
  })
}
