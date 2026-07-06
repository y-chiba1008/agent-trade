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
import { formatJpy } from '@/features/common/money'
import { useExecutionsQuery } from '@/features/execution/list/useExecutionsQuery'

type ExecutionHistoryTableProps = {
  accountId: number
}

export function ExecutionHistoryTable({
  accountId,
}: ExecutionHistoryTableProps) {
  const {
    data: executions,
    isLoading,
    isError,
    error,
  } = useExecutionsQuery(accountId)

  if (isLoading) {
    return <p className="text-sm text-muted-foreground">約定履歴を読み込み中...</p>
  }

  if (isError) {
    return (
      <p className="text-sm text-destructive">
        約定履歴の取得に失敗しました:{' '}
        {error instanceof ApiError ? error.detail : error?.message}
      </p>
    )
  }

  if (!executions || executions.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">約定履歴はありません。</p>
    )
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>注文ID</TableHead>
          <TableHead>数量</TableHead>
          <TableHead>価格</TableHead>
          <TableHead>約定日時</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {executions.map((execution) => (
          <TableRow key={execution.id}>
            <TableCell>{execution.id}</TableCell>
            <TableCell>{execution.order_id}</TableCell>
            <TableCell>{execution.quantity}</TableCell>
            <TableCell>{formatJpy(execution.price)}</TableCell>
            <TableCell>{formatDateTime(execution.executed_at)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
