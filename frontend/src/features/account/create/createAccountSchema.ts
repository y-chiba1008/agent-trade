import { z } from 'zod'

export const createAccountSchema = z.object({
  name: z
    .string()
    .min(1, '名称は1文字以上で入力してください')
    .max(100, '名称は100文字以内で入力してください'),
  account_tag: z.enum(['human', 'ai']),
  initial_jpy_balance: z
    .number({ error: '数値を入力してください' })
    .int('整数で入力してください')
    .min(0, '0以上の値を入力してください'),
})

export type CreateAccountFormValues = z.infer<typeof createAccountSchema>
