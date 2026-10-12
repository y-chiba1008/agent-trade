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
import {
  createAccountSchema,
  type CreateAccountFormValues,
} from '@/features/account/create/createAccountSchema'
import { useCreateAccountMutation } from '@/features/account/create/useCreateAccountMutation'

export function CreateAccountForm() {
  const [successMessage, setSuccessMessage] = useState<string | null>(null)
  const createAccountMutation = useCreateAccountMutation()

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<CreateAccountFormValues>({
    resolver: zodResolver(createAccountSchema),
    defaultValues: {
      name: '',
      account_tag: 'human',
      initial_jpy_balance: 1000000,
    },
  })

  const accountTag = watch('account_tag')

  const onSubmit = handleSubmit(async (values) => {
    setSuccessMessage(null)
    try {
      const account = await createAccountMutation.mutateAsync(values)
      reset({
        name: '',
        account_tag: 'human',
        initial_jpy_balance: 1000000,
      })
      setSuccessMessage(`口座「${account.name}」を作成しました`)
    } catch {
      // mutation error はフォーム下で表示
    }
  })

  const submitError =
    createAccountMutation.error instanceof ApiError
      ? createAccountMutation.error.detail
      : createAccountMutation.error instanceof Error
        ? createAccountMutation.error.message
        : null

  return (
    <Card>
      <CardHeader>
        <CardTitle>口座を作成</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">口座名</Label>
            <Input id="name" {...register('name')} />
            {errors.name && (
              <p className="text-sm text-destructive">{errors.name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="account_tag">用途タグ</Label>
            <Select
              value={accountTag}
              onValueChange={(value) => {
                if (value === 'human' || value === 'ai') {
                  setValue('account_tag', value, { shouldValidate: true })
                }
              }}
            >
              <SelectTrigger id="account_tag" className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="human">human（人間用）</SelectItem>
                <SelectItem value="ai">ai（AI用）</SelectItem>
              </SelectContent>
            </Select>
            {errors.account_tag && (
              <p className="text-sm text-destructive">
                {errors.account_tag.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="initial_jpy_balance">初期資金（JPY）</Label>
            <Input
              id="initial_jpy_balance"
              type="number"
              min={0}
              {...register('initial_jpy_balance', { valueAsNumber: true })}
            />
            {errors.initial_jpy_balance && (
              <p className="text-sm text-destructive">
                {errors.initial_jpy_balance.message}
              </p>
            )}
          </div>

          {submitError && (
            <p className="text-sm text-destructive">{submitError}</p>
          )}
          {successMessage && (
            <p className="text-sm text-green-600">{successMessage}</p>
          )}

          <Button type="submit" disabled={createAccountMutation.isPending}>
            {createAccountMutation.isPending ? '作成中...' : '口座を作成'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
