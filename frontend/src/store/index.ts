import { store } from 'quasar/wrappers'
import Vuex from 'vuex'
import VueCookies from 'vue-cookies'
import authModule from './modules/auth'
import performanceReviewModule from './modules/performancereview'
import responsibilityModule from './modules/responsibility'
import securityMessageModule from './modules/securitymessage'
import teleworkModule from './modules/telework'
import userModule from './modules/user'


// import example from './module-example';
// import { ExampleStateInterface } from './module-example/state';

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

// TODO: https://betterprogramming.pub/the-state-of-typed-vuex-the-cleanest-approach-2358ee05d230

export interface StateInterface {
  // Define your own store structure, using submodules if needed
  // example: ExampleStateInterface;
  // Declared as unknown to avoid linting issue. Best to strongly type as per the line above.
  example: unknown;
}

export default store(function ({ Vue }) {
  Vue.use(Vuex)
  Vue.use(VueCookies)

  const Store = new Vuex.Store<StateInterface>({
    modules: {
      authModule,
      userModule,
      performanceReviewModule,
      responsibilityModule,
      securityMessageModule,
      teleworkModule,
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: !!process.env.DEV
  });

  return Store;
});
