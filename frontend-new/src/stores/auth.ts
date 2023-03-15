import { defineStore } from 'pinia';
import { Stop, AxiosAuthResponse, UserRetrieve } from 'src/types';
import axios from 'axios';
import { useUserStore } from './user';

// TODO
// const apiURL = process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/'
const apiURL = 'http://localhost:8000/'
const userStore = useUserStore()

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('-token') || '',
    status: '',
  }),

  getters: {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status
  },

  actions: {
    // Old way of logging in via /auth/login
    authRequest: (user: UserRetrieve) => {
      return new Promise((resolve, reject) => { // The Promise used for router redirect in login
        debugger
        commit('authRequest')
        axios({url: `${ process.env.API_URL }api/api-token-auth-password/`, data: user, method: 'POST' }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
          .then((resp: AxiosAuthResponse) => {
            const token = resp.data.token
            localStorage.setItem('user-token', token) // store the token in localstorage
            axios.defaults.headers.common['Authorization'] = `Token ${token}` // eslint-disable-line @typescript-eslint/no-unsafe-member-access
            commit('authSuccess', token)
            // you have your token, now log in your user :)
            dispatch('userModule/userRequest', null, { root: true })
              .catch(err => console.log(err))
            resolve(resp)
          })
        .catch(err => {
          commit('authError', err) // TODO: Mutation doesn't need err
          localStorage.removeItem('user-token') // if the request fails, remove any possible user token if possible
          reject(err)
        })
      })
    },
    // Log in with Microsoft Azure SSO
    setAuth(user: UserRetrieve) {
      return new Promise((resolve, reject) => { // The Promise used for router redirect in login
        this.status = 'loading'
        axios({url: `${ process.env.API_URL }api/api-token-auth/`, data: user, method: 'POST' }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
          .then((resp: AxiosAuthResponse) => {
            const token = resp.data.token
            localStorage.setItem('user-token', token) // store the token in localstorage
            axios.defaults.headers.common['Authorization'] = `Token ${token}` // eslint-disable-line @typescript-eslint/no-unsafe-member-access
            this.status = 'success'
            this.token = token
            // you have your token, now log in your user :)
            userStore.userRequest()
              .catch(err => console.log(err))
            resolve(resp)
          })
        .catch(err => {
          this.status = 'error'
          localStorage.removeItem('user-token') // if the request fails, remove any possible user token if possible
          reject(err)
        })
      })
    },
    authLogout: () => {
      return new Promise((resolve) => {
        commit('authLogout')
        dispatch('mealsModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('peopleModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('performanceReviewModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('responsibilityModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('securityMessageModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('teleworkModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('timeOffModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('userModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        dispatch('workflowModule/authLogout', null, { root: true })
          .catch(err => console.log(err))
        localStorage.removeItem('user-token') // clear your user's token from localstorage
        resolve('Successfully logged user out')
      })
    }
  }
});
