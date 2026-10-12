import { format, parseISO } from 'date-fns'
import { ja } from 'date-fns/locale'

export function formatDateTime(isoString: string): string {
  return format(parseISO(isoString), 'yyyy/MM/dd HH:mm:ss', { locale: ja })
}
