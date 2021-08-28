import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { SecurityMessageStateInterface } from './state';
import axios from 'axios';
import { ViewedSecurityMessageCreate } from 'src/store/types';

const actions: ActionTree<SecurityMessageStateInterface, StateInterface> = {
  getViewedLatestSecurityMessage: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/viewedsecuritymessage/employee_viewed_latest_security_message` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setViewedLatestSecurityMessage', resp);
      })
      .catch(e => {
        console.error('Error getting viewed security messages:', e)
      });
  },
  getViewedSecurityMessages: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/viewedsecuritymessage` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setViewedSecurityMessages', resp);
      })
      .catch(e => {
        console.error('Error getting viewed security messages:', e)
      });
  },
  setViewedSecurityMessage: ({ dispatch }, viewedSecurityMessage: ViewedSecurityMessageCreate) => {
    axios({ url: `${ process.env.API_URL }api/v1/viewedsecuritymessage`, data: viewedSecurityMessage, method: 'POST' }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(() => {
        dispatch('getViewedLatestSecurityMessage')
          .catch(e => {
            console.error('Error getting all viewed security messages ater marking one as viewed:', e)
          })
        dispatch('getViewedSecurityMessages')
          .catch(e => {
            console.error('Error getting all viewed security messages ater marking one as viewed:', e)
          })
      })
      .catch(e => {
        console.error('Error marking a security message as viewed:', e)
      });
  },
  authLogout: ({commit}) => {
    return new Promise((resolve) => {
      commit('authLogout')
      resolve()
    })
  }
};

export default actions;
