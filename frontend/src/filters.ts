import { date } from 'quasar'

export function first4Chars(str: string) {
  return str.substring(0, 4)
}

export function last4Chars(str: string) {
  return str.substring(str.length - 4)
}


// Trying a new tack. We don't actually care about timezones in the database,
// we just want to display the date in the user's timezone.

export function readableDateNEW(d: string): string {
  // d should be a string in the format 'YYYY-MM-DD'
  if (!d) {
    return 'Date not set'
  }
  try {
    const parts = d.split('-') // ['YYYY', 'MM', 'DD']
    return `${parts[1]}/${parts[2]}/${parts[0]}` // 'MM/DD/YYYY'
  }
  catch (e) {
    return 'Date ' + d + 'incorrectly formatted: ' + e
  }
}

// Existing date handling which attempts to adjust for timezone. The theory was
// we would store dates in UTC and then adjust them to the user's timezone, but
// that's confusing and not necessary.

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
