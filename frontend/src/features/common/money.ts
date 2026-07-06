export function formatJpy(amount: number): string {
  return new Intl.NumberFormat('ja-JP', {
    style: 'currency',
    currency: 'JPY',
    maximumFractionDigits: 0,
  }).format(amount)
}

export function formatBtc(amount: string): string {
  const value = Number(amount)
  if (Number.isNaN(value)) {
    return amount
  }
  return `${value.toLocaleString('ja-JP', { maximumFractionDigits: 8 })} BTC`
}
