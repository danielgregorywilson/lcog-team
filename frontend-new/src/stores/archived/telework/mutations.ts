import { TeleworkApplicationRetrieve } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { TeleworkStateInterface } from './state'


const mutation: MutationTree<TeleworkStateInterface> = {
  setTeleworkApplication: (state, resp: {data: TeleworkApplicationRetrieve}) => {
    Vue.set(state, 'teleworkApplication', resp.data)
  },
  setAllTeleworkApplicationsSignatureRequired: (state, resp: {data: Array<TeleworkApplicationRetrieve>}) => {
    Vue.set(state, 'allTeleworkApplicationsSignatureRequired', resp.data)
  },
  setAllTeleworkApplicationsSignatureNotRequired: (state, resp: {data: Array<TeleworkApplicationRetrieve>}) => {
    Vue.set(state, 'allTeleworkApplicationsSignatureNotRequired', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.teleworkApplication = {pk: undefined, employee_pk: undefined, employee_name: '', status: ''}
    state.allTeleworkApplicationsSignatureRequired = []
    state.allTeleworkApplicationsSignatureNotRequired = []
  }
};

export default mutation;
