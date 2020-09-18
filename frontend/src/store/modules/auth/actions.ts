import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { AuthStateInterface } from './state';
import axios from 'axios';

const actions: ActionTree<AuthStateInterface, StateInterface> = {
  authRequest: ({commit, dispatch}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('authRequest')
      axios({url: 'http://localhost:8000/api/api-token-auth/', data: user, method: 'POST' })
        .then(resp => {
          const token = resp.data.token
          localStorage.setItem('user-token', token) // store the token in localstorage
          axios.defaults.headers.common['Authorization'] = 'Token ' + token
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
  authLogout: ({commit, dispatch}) => {
    return new Promise((resolve, reject) => {
      commit('authLogout')
      localStorage.removeItem('user-token') // clear your user's token from localstorage
      resolve()
    })
  }
};

export default actions;
