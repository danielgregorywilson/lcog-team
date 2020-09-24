import { off } from 'process'
import Vue from 'vue'

Vue.filter('first4Chars', (str: string) => str.substring(0, 4))
Vue.filter('last4Chars', (str: string) => str.substring(str.length - 4))
Vue.filter('readableDate', (d: Date) => {
  const date = new Date(d) // Date from server (adjusted to our timezone)
  const offsetMins = date.getTimezoneOffset() // Number of minutes behind server time we are
  const offsetMsecs = offsetMins*60000 // Number of milliseconds
  return new Date(date.getTime() + offsetMsecs).toLocaleDateString()
})
