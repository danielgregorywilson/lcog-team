import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { AuthStateInterface } from './state';
import axios from 'axios';
import { AxiosAuthResponse, UserRetrieve } from 'src/store/types';

const actions: ActionTree<AuthStateInterface, StateInterface> = {
  authRequest: ({commit, dispatch}, user: UserRetrieve) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('authRequest')
      // axios({url: 'http://localhost:8000/api/api-token-auth/', data: user, method: 'POST' })
      axios({url: 'http://lcog-internal-env.eba-4t9yrmiu.us-west-2.elasticbeanstalk.com/api/api-token-auth/', data: user, method: 'POST' })
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
  authLogout: ({commit}) => {
    return new Promise((resolve) => {
      commit('authLogout')
      localStorage.removeItem('user-token') // clear your user's token from localstorage
      resolve()
    })
  }
};

export default actions;
