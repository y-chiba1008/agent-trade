import { zodResolver } from '@hookform/resolvers/zod'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { ApiError } from '@/api/client'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { formatJpy } from '@/features/common/money'
import {
  marketOrderSchema,
  type MarketOrderFormValues,
} from '@/features/order/placeMarket/marketOrderSchema'
import { usePlaceMarketOrderMutation } from '@/features/order/placeMarket/usePlaceMarketOrderMutation'
import type { PlacedMarketOrderResult } from '@/features/order/shared/orderTypes'

type MarketOrderFormProps = {
  accountId: number
}

export function MarketOrderForm({ accountId }: MarketOrderFormProps) {
  const [successResult, setSuccessResult] =
    useState<PlacedMarketOrderResult | null>(null)
  const placeOrderMutation = usePlaceMarketOrderMutation()

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<MarketOrderFormValues>({
    resolver: zodResolver(marketOrderSchema),
    defaultValues: {
      side: 'buy',
      quantity: '0.001',
    },
  })

  const side = watch('side')

  const onSubmit = handleSubmit(async (values) => {
    setSuccessResult(null)
    try {
      const result = await placeOrderMutation.mutateAsync({
        accountId,
        input: values,
      })
      setSuccessResult(result)
      reset({ side: values.side, quantity: values.quantity })
    } catch {
      // mutation error はフォーム下で表示
    }
  })

  const submitError =
    placeOrderMutation.error instanceof ApiError
      ? placeOrderMutation.error.detail
      : placeOrderMutation.error instanceof Error
        ? placeOrderMutation.error.message
        : null

  return (
    <Card>
      <CardHeader>
        <CardTitle>成行注文</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="side">売買</Label>
            <Select
              value={side}
              onValueChange={(value) => {
                if (value === 'buy' || value === 'sell') {
                  setValue('side', value, { shouldValidate: true })
                }
              }}
            >
              <SelectTrigger id="side" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="buy">買い</SelectItem>
                <SelectItem value="sell">売り</SelectItem>
              </SelectContent>
            </Select>
            {errors.side && (
              <p className="text-sm text-destructive">{errors.side.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="quantity">数量（BTC）</Label>
            <Input id="quantity" {...register('quantity')} />
            {errors.quantity && (
              <p className="text-sm text-destructive">
                {errors.quantity.message}
              </p>
            )}
          </div>

          {submitError && (
            <p className="text-sm text-destructive">{submitError}</p>
          )}
          {successResult && (
            <p className="text-sm text-green-600">
              約定しました（価格: {formatJpy(successResult.execution_price_jpy)}、
              新JPY残高: {formatJpy(successResult.new_jpy_balance)}）
            </p>
          )}

          <Button type="submit" disabled={placeOrderMutation.isPending}>
            {placeOrderMutation.isPending ? '注文中...' : '成行注文を出す'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
