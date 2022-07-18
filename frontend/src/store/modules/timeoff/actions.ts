import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { TimeOffRequestStateInterface } from './state';
import axios from 'axios';
import { TimeOffRequestAcknowledge, TimeOffRequestCreate } from 'src/store/types';

const actions: ActionTree<TimeOffRequestStateInterface, StateInterface> = {
  getMyTimeOffRequests: ({ commit }) => {
    axios({ url: `${ process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/' }api/v1/timeoffrequest` })
      .then(resp => {
        commit('setMyTimeOffRequests', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getManagedTimeOffRequests: ({ commit }) => {
    axios({ url: `${ process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/' }api/v1/timeoffrequest?managed=True` })
      .then(resp => {
        commit('setManagedTimeOffRequests', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  createTimeOffRequest: ({ dispatch }, timeOffRequest: TimeOffRequestCreate) => {
    axios({ url: `${ process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/' }api/v1/timeoffrequest`, data: timeOffRequest, method: 'POST' })
      .then(() => {
        dispatch('getMyTimeOffRequests')
          .catch(e => {
            console.log(e)
          })
      })
      .catch(e => {
        console.log(e)
      });
  },
};

export default actions;
