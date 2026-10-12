import { Link } from 'react-router'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
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
import { formatBtc, formatJpy } from '@/features/common/money'
import { CreateAccountForm } from '@/features/account/create/createAccountForm'
import { useDeleteAccountMutation } from '@/features/account/delete/useDeleteAccountMutation'
import { useAccountsQuery } from '@/features/account/list/useAccountsQuery'

export function AccountListPage() {
  const { data: accounts, isLoading, isError, error } = useAccountsQuery()
  const deleteAccountMutation = useDeleteAccountMutation()

  const handleDelete = async (accountId: number) => {
    await deleteAccountMutation.mutateAsync(accountId)
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">デモ口座一覧</h2>
        <p className="text-sm text-muted-foreground">
          デモ口座の作成・管理を行います。
        </p>
      </div>

      <CreateAccountForm />

      <Card>
        <CardHeader>
          <CardTitle>口座一覧</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading && <p className="text-sm text-muted-foreground">読み込み中...</p>}

          {isError && (
            <p className="text-sm text-destructive">
              口座一覧の取得に失敗しました:{' '}
              {error instanceof ApiError ? error.detail : error?.message}
            </p>
          )}

          {!isLoading && !isError && accounts?.length === 0 && (
            <p className="text-sm text-muted-foreground">
              口座がありません。上のフォームから作成してください。
            </p>
          )}

          {!isLoading && !isError && accounts && accounts.length > 0 && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>名称</TableHead>
                  <TableHead>タグ</TableHead>
                  <TableHead>JPY残高</TableHead>
                  <TableHead>BTC残高</TableHead>
                  <TableHead>作成日時</TableHead>
                  <TableHead className="text-right">操作</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {accounts.map((account) => (
                  <TableRow key={account.id}>
                    <TableCell>{account.id}</TableCell>
                    <TableCell>{account.name}</TableCell>
                    <TableCell>
                      <Badge variant="secondary">{account.account_tag}</Badge>
                    </TableCell>
                    <TableCell>{formatJpy(account.jpy_balance)}</TableCell>
                    <TableCell>{formatBtc(account.btc_balance)}</TableCell>
                    <TableCell>{formatDateTime(account.created_at)}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          nativeButton={false}
                          render={<Link to={`/accounts/${account.id}`} />}
                        >
                          詳細
                        </Button>
                        <AlertDialog>
                          <AlertDialogTrigger
                            render={
                              <Button
                                variant="destructive"
                                size="sm"
                                disabled={deleteAccountMutation.isPending}
                              />
                            }
                          >
                            削除
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>口座を削除しますか？</AlertDialogTitle>
                              <AlertDialogDescription>
                                口座「{account.name}」（ID: {account.id}）を削除します。この操作は取り消せません。
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel>キャンセル</AlertDialogCancel>
                              <AlertDialogAction
                                onClick={() => void handleDelete(account.id)}
                              >
                                削除する
                              </AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
