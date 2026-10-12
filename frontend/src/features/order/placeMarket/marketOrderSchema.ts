import { z } from 'zod'

export const marketOrderSchema = z.object({
  side: z.enum(['buy', 'sell']),
  quantity: z
    .string()
    .min(1, '数量を入力してください')
    .refine((value) => {
      const num = Number(value)
      return !Number.isNaN(num) && num > 0
    }, '0より大きい数値を入力してください'),
})

export type MarketOrderFormValues = z.infer<typeof marketOrderSchema>
