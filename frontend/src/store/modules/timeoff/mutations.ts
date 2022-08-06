import TimeOffRequest from 'src/pages/timeoff/NewRequest.vue';
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { TimeOffRequestStateInterface } from './state'


const mutation: MutationTree<TimeOffRequestStateInterface> = {
  setMyTimeOffRequests: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'myTimeOffRequests', resp.data)
  },
  setTeamTimeOffRequests: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'teamTimeOffRequests', resp.data)
  },
  setManagedTimeOffRequests: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'managedTimeOffRequests', resp.data)
  },
  setConflictingResponsibilities: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'conflictingTimeOffRequests', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.myTimeOffRequests = []
    state.teamTimeOffRequests = []
    state.managedTimeOffRequests = []
    state.conflictingTimeOffRequests = []
  }
};

export default mutation;
