import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { ResponsibilityStateInterface } from './state';
import axios from 'axios';
import {
  AxiosTeleworkApplicationRetrieveOneServerResponse,
  TeleworkSignatureCreate
} from 'src/store/types';

function getApiUrl(): string {
  if (process.env.API_URL) {
    return process.env.API_URL
  } else {
    return ''
  }
}

const actions: ActionTree<ResponsibilityStateInterface, StateInterface> = {
  getAllResponsibilities: ({ commit }) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/responsibilities` })
        .then(resp => {
          commit('setAllResponsibilities', resp)
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting all responsibilities:', e)
          reject(e)
        })
    })
  },
  getOrphanedResponsibilities: ({ commit }) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/responsibilities?orphaned=True` })
        .then(resp => {
          commit('setOrphanedResponsibilities', resp)
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting orphaned responsibilities:', e)
          reject(e)
        })
    })
  },
  getEmployeePrimaryResponsibilities: ({ commit }, data: {pk: number}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/responsibilities?employee=${ data.pk }` })
        .then(resp => {
          commit('setEmployeePrimaryResponsibilities', {employeePk: data.pk, responsibilities: resp})
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting employee primary responsibilities:', e)
          reject(e)
        })
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
