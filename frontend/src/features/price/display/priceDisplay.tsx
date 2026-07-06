import { usePriceQuery } from '@/features/price/display/usePriceQuery'
import { formatJpy } from '@/features/common/money'
import { formatDateTime } from '@/features/common/dateFormat'

export function PriceDisplay() {
  const { data, isLoading, isError, error } = usePriceQuery()

  if (isLoading) {
    return <span className="text-sm text-muted-foreground">価格取得中...</span>
  }

  if (isError) {
    return (
      <span className="text-sm text-destructive">
        価格取得エラー: {error instanceof Error ? error.message : '不明なエラー'}
      </span>
    )
  }

  if (!data) {
    return <span className="text-sm text-muted-foreground">価格未取得</span>
  }

  return (
    <div className="text-right text-sm">
      <div className="font-medium">
        BTC/JPY {formatJpy(data.price_jpy)}
      </div>
      <div className="text-xs text-muted-foreground">
        更新: {formatDateTime(data.timestamp)}
      </div>
    </div>
  )
}
