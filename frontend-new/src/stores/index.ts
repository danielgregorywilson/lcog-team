import { store } from 'quasar/wrappers'
import { createPinia } from 'pinia'
import { Router } from 'vue-router'

/*
 * When adding new properties to stores, you should also
 * extend the `PiniaCustomProperties` interface.
 * @see https://pinia.vuejs.org/core-concepts/plugins.html#typing-new-store-properties
 */
declare module 'pinia' {
  export interface PiniaCustomProperties {
    readonly router: Router
  }
}

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default store((/* { ssrContext } */) => {
  const pinia = createPinia()

  // You can add Pinia plugins here
  // pinia.use(SomePiniaPlugin)

  return pinia
})

export function handlePromiseError(reject: (reason?: any) => void, message: string, error: string) { // eslint-disable-line @typescript-eslint/no-explicit-any
  const errorMessage = `${ message }: ${ error }`
  console.error(errorMessage)
  reject(errorMessage)
}

export const apiURL = process.env.API_URL ?
  process.env.API_URL : 'https://api.team.lcog.org/'