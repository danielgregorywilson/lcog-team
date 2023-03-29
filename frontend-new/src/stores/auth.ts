import { defineStore } from 'pinia';
import { AuthStateInterface, AxiosAuthResponse } from 'src/types';
import axios from 'axios';
import { useMealsStore } from './meals';
import { usePeopleStore } from './people';
import { useTimeOffStore } from './timeoff';
import { useUserStore } from './user';


const apiURL = process.env.API_URL ? 
  process.env.API_URL : 'https://api.team.lcog.org/'
const mealsStore = useMealsStore()
const peopleStore = usePeopleStore()
const timeOffStore = useTimeOffStore()
const userStore = useUserStore()


export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('user-token') || '',
    status: '',
  }),

  getters: {
    isAuthenticated: state => !!state.token
  },

  actions: {
    // Log in with username and password
    authWithUsername(user: {username: string, password: string}) {
      return this.authenticate(user, `${ apiURL }api/api-token-auth-password/`)
    },
    // Log in with Microsoft Azure SSO
    authWithMicrosoft(user: { username: string, firstName: string, lastName: string }) {
      return this.authenticate(user, `${ apiURL }api/api-token-auth/`)
    },
    authenticate(
      user: { username: string, password: string } | 
        { username: string, firstName: string, lastName: string },
      url: string
    ) {
      return new Promise((resolve, reject) => {
        this.status = 'loading'
        axios({url: url, data: user, method: 'POST'})
          .then((resp: AxiosAuthResponse) => {
            const token = resp.data.token
            localStorage.setItem('user-token', token)
            axios.defaults.headers.common['Authorization'] = `Token ${token}`
            this.status = 'success'
            this.token = token
            // you have your token, now log in your user :)
            userStore.userRequest()
              .catch(err => console.log(err))
            resolve(resp)
          })
        .catch(err => {
          this.status = 'error'
          // if the request fails, remove any possible user token
          localStorage.removeItem('user-token')
          reject(err)
        })
      })
    },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        localStorage.removeItem('user-token') // clear your user's token from localstorage
        mealsStore.authLogout()
          .catch(err => console.log(err))
        peopleStore.authLogout()
          .catch(err => console.log(err))
        // TODO: Uncomment these when the modules are ready
        // dispatch('performanceReviewModule/authLogout', null, { root: true })
        //   .catch(err => console.log(err))
        // dispatch('responsibilityModule/authLogout', null, { root: true })
        //   .catch(err => console.log(err))
        // dispatch('securityMessageModule/authLogout', null, { root: true })
        //   .catch(err => console.log(err))
        // dispatch('teleworkModule/authLogout', null, { root: true })
        //   .catch(err => console.log(err))
        timeOffStore.authLogout()
          .catch(err => console.log(err))
        userStore.authLogout()
          .catch(err => console.log(err))
        // dispatch('workflowModule/authLogout', null, { root: true })
        //   .catch(err => console.log(err))
        
        resolve('Successfully logged user out')
      })
    }
  }
});
