import { Link, useParams } from 'react-router'
import { ApiError } from '@/api/client'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { formatDateTime } from '@/features/common/dateFormat'
import { formatBtc, formatJpy } from '@/features/common/money'
import { useAccountsQuery } from '@/features/account/list/useAccountsQuery'
import { ExecutionHistoryTable } from '@/features/execution/list/executionHistoryTable'
import { MarketOrderForm } from '@/features/order/placeMarket/marketOrderForm'
import { OrderHistoryTable } from '@/features/order/list/orderHistoryTable'

export function AccountDetailPage() {
  const { accountId: accountIdParam } = useParams()
  const accountId = Number(accountIdParam)
  const isValidAccountId = Number.isInteger(accountId) && accountId > 0

  const { data: accounts, isLoading, isError, error } = useAccountsQuery()

  if (!isValidAccountId) {
    return (
      <p className="text-sm text-destructive">無効な口座IDです。</p>
    )
  }

  if (isLoading) {
    return <p className="text-sm text-muted-foreground">口座情報を読み込み中...</p>
  }

  if (isError) {
    return (
      <p className="text-sm text-destructive">
        口座情報の取得に失敗しました:{' '}
        {error instanceof ApiError ? error.detail : error?.message}
      </p>
    )
  }

  const account = accounts?.find((item) => item.id === accountId)

  if (!account) {
    return (
      <div className="space-y-4">
        <p className="text-sm text-destructive">
          口座 ID {accountId} が見つかりません。
        </p>
        <Button variant="outline" render={<Link to="/" />}>
          口座一覧に戻る
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-semibold">{account.name}</h2>
          <p className="text-sm text-muted-foreground">
            口座 ID: {account.id} / 作成: {formatDateTime(account.created_at)}
          </p>
        </div>
        <Button variant="outline" render={<Link to="/" />}>
          口座一覧に戻る
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            残高
            <Badge variant="secondary">{account.account_tag}</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-1">
          <p>JPY: {formatJpy(account.jpy_balance)}</p>
          <p>BTC: {formatBtc(account.btc_balance)}</p>
        </CardContent>
      </Card>

      <MarketOrderForm accountId={accountId} />

      <Card>
        <CardHeader>
          <CardTitle>注文履歴</CardTitle>
        </CardHeader>
        <CardContent>
          <OrderHistoryTable accountId={accountId} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>約定履歴</CardTitle>
        </CardHeader>
        <CardContent>
          <ExecutionHistoryTable accountId={accountId} />
        </CardContent>
      </Card>
    </div>
  )
}
