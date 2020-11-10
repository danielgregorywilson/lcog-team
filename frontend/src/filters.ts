import Vue from 'vue'

Vue.filter('first4Chars', (str: string) => str.substring(0, 4))
Vue.filter('last4Chars', (str: string) => str.substring(str.length - 4))

// Could use Quasar Date utils here to make it nicer
// https://quasar.dev/quasar-utils/date-utils
Vue.filter('readableDate', (d: Date) => {
  if (!d) {
    return 'Date not set'
  }
  
  const readableDate = new Date(d) // Date from server (adjusted to our timezone)
  const offsetMins = readableDate.getTimezoneOffset() // Number of minutes behind server time we are
  const offsetMsecs = offsetMins*60000 // Number of milliseconds
  return new Date(readableDate.getTime() + offsetMsecs).toLocaleDateString()
})
