import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { TimeOffRequestStateInterface } from './state';
import axios from 'axios';
import { TimeOffRequestAcknowledge, TimeOffRequestCreate, TimeOffRequestDates } from 'src/store/types';

const apiURL = process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/'

const actions: ActionTree<TimeOffRequestStateInterface, StateInterface> = {
  getMyTimeOffRequests: ({ commit }) => {
    axios({ url: `${ apiURL }api/v1/timeoffrequest` })
      .then(resp => {
        commit('setMyTimeOffRequests', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getTeamTimeOffRequests: ({ commit }) => {
    axios({ url: `${ apiURL }api/v1/timeoffrequest?team=True` })
      .then(resp => {
        commit('setTeamTimeOffRequests', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getManagedTimeOffRequests: ({ commit }) => {
    axios({ url: `${ apiURL }api/v1/timeoffrequest?managed=True` })
      .then(resp => {
        commit('setManagedTimeOffRequests', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getConflictingResponsibilities: ({ commit }, data: { dates: Array<TimeOffRequestDates>}) => {
    axios({ url: `${ apiURL }api/v1/timeoffrequest/conflicting_responsibilities`, data: data, method: 'POST' })
      .then(resp => {
        commit('setConflictingResponsibilities', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  createTimeOffRequest: ({ dispatch }, timeOffRequest: TimeOffRequestCreate) => {
    axios({ url: `${ apiURL }api/v1/timeoffrequest`, data: timeOffRequest, method: 'POST' })
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
  acknowledgeTimeOffRequest: ({ dispatch }, timeOffRequest: TimeOffRequestAcknowledge) => {
    axios({ url: `${ apiURL }api/v1/timeoffrequest`, data: timeOffRequest, method: 'PUT' })
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
