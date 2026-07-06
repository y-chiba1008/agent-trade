export type AccountTag = 'human' | 'ai'

export type Account = {
  id: number
  name: string
  account_tag: AccountTag
  jpy_balance: number
  btc_balance: string
  created_at: string
  updated_at: string
}

export type CreateAccountInput = {
  name: string
  account_tag: AccountTag
  initial_jpy_balance: number
}
