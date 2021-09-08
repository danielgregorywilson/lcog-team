import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { UserStateInterface } from './state';
import axios from 'axios';

const actions: ActionTree<UserStateInterface, StateInterface> = {
  // For requesting user on login
  userRequest: ({ commit, dispatch }) => {
    return new Promise((resolve, reject) => {
      commit('userRequest');
      axios({ url: `${ process.env.API_URL }api/v1/current-user/` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
        .then((resp: {data: {pk: number}}) => {
          commit('userSuccess', resp);
          dispatch('performanceReviewModule/getNextPerformanceReview', {pk: resp.data.pk}, { root: true })
            .catch(err => console.log(err))
          dispatch('securityMessageModule/getViewedLatestSecurityMessage', {}, { root: true })
            .catch(err => console.log(err))
          resolve(resp)
        })
        .catch(e => {
          commit('userError');
          // if resp is unauthorized, logout, to
          dispatch('authLogout')
            .catch(err => console.log(err))
          reject(e)
        });
    })
  },
  // For getting just the user on specific pages
  simpleUserRequest: () => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ process.env.API_URL }api/v1/current-user/` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
        .then((resp: {data: {pk: number}}) => {
          resolve(resp)
        })
        .catch(e => {
          reject(e)
        });
    })
  },
  authLogout: ({commit}) => {
    return new Promise((resolve) => {
      commit('authLogout')
      resolve('Successfully triggered logout')
    })
  }
};

export default actions;
