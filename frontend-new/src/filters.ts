export function first4Chars(str: string) {
  return str.substring(0, 4)
}

export function last4Chars(str: string) {
  return str.substring(str.length - 4)
}

// Could use Quasar Date utils here to make it nicer
// https://quasar.dev/quasar-utils/date-utils
export function readableDate(d: Date): string {
  if (!d) {
    return 'Date not set'
  }
  const readableDate = new Date(d) // Date from server (adjusted to our timezone)
  const offsetMins = readableDate.getTimezoneOffset() // Number of minutes behind server time we are
  const offsetMsecs = offsetMins*60000 // Number of milliseconds
  return new Date(readableDate.getTime() + offsetMsecs).toLocaleDateString()
}

export function readableDateTime(d: Date): string {
  if (!d) {
    return 'Date not set'
  }
  const readableDate = new Date(d) // Date from server (adjusted to our timezone)
  return new Date(readableDate.getTime()).toLocaleString()
}
