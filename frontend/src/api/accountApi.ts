import { apiRequest } from '@/api/client'
import type { Account, CreateAccountInput } from '@/features/account/shared/accountTypes'

export function listAccounts(): Promise<Account[]> {
  return apiRequest<Account[]>('/accounts')
}

export function createAccount(input: CreateAccountInput): Promise<Account> {
  return apiRequest<Account>('/accounts', {
    method: 'POST',
    body: input,
  })
}

export function deleteAccount(accountId: number): Promise<void> {
  return apiRequest<void>(`/accounts/${accountId}`, {
    method: 'DELETE',
  })
}
