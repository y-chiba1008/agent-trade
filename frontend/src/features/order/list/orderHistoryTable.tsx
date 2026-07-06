import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { ApiError } from '@/api/client'
import { formatDateTime } from '@/features/common/dateFormat'
import { useOrdersQuery } from '@/features/order/list/useOrdersQuery'

type OrderHistoryTableProps = {
  accountId: number
}

export function OrderHistoryTable({ accountId }: OrderHistoryTableProps) {
  const { data: orders, isLoading, isError, error } = useOrdersQuery(accountId)

  if (isLoading) {
    return <p className="text-sm text-muted-foreground">注文履歴を読み込み中...</p>
  }

  if (isError) {
    return (
      <p className="text-sm text-destructive">
        注文履歴の取得に失敗しました:{' '}
        {error instanceof ApiError ? error.detail : error?.message}
      </p>
    )
  }

  if (!orders || orders.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">注文履歴はありません。</p>
    )
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>種別</TableHead>
          <TableHead>売買</TableHead>
          <TableHead>数量</TableHead>
          <TableHead>状態</TableHead>
          <TableHead>日時</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {orders.map((order) => (
          <TableRow key={order.id}>
            <TableCell>{order.id}</TableCell>
            <TableCell>{order.order_type}</TableCell>
            <TableCell>{order.side}</TableCell>
            <TableCell>{order.quantity}</TableCell>
            <TableCell>{order.status}</TableCell>
            <TableCell>{formatDateTime(order.created_at)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
