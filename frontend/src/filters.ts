import { date } from 'quasar'

export function first4Chars(str: string) {
  return str.substring(0, 4)
}

export function last4Chars(str: string) {
  return str.substring(str.length - 4)
}

export function readableDate(d: Date): string {
  if (!d) {
    return 'Date not set'
  }
  const localDate = new Date(d) // Date from server (adjusted to our timezone)
  return date.formatDate(localDate, 'M/D/YYYY') // Format with Quasar date util
}

export function readableDateTime(d: Date | string): string {
  if (!d) {
    return 'Date not set'
  }
  const readableDate = new Date(d) // Date from server (adjusted to our timezone)
  return new Date(readableDate.getTime()).toLocaleString()
}
