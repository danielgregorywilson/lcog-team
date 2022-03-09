import { ActionTree } from 'vuex'
import { StateInterface } from '../../index'
import { ResponsibilityStateInterface } from '../../types'
import axios from 'axios'

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
      axios({ url: `${ getApiUrl() }api/v1/responsibilities?orphaned=true` })
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
  getEmployeeSecondaryResponsibilities: ({ commit }, data: {pk: number}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/responsibilities?employee=${ data.pk }&secondary=true` })
        .then(resp => {
          commit('setEmployeeSecondaryResponsibilities', {employeePk: data.pk, responsibilities: resp})
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting employee secondary responsibilities:', e)
          reject(e)
        })
    })
  },
  getAllTags: ({ commit }) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/responsibilitytags` })
        .then(resp => {
          commit('setAllTags', resp)
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting all tags:', e)
          reject(e)
        })
    })
  },
  getSimpleEmployeeList: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/employee/simple_list`}) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setSimpleEmployeeList', resp)
      })
      .catch(e => {
        console.error('Error getting simple employee list:', e)
      })
  },
  getSimpleEmployeeDetail: ({ commit }, data: {pk: number}) => {
    axios({ url: `${ process.env.API_URL }api/v1/employee/${ data.pk }/simple_detail`}) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setSimpleEmployeeDetail', resp)
      })
      .catch(e => {
        console.error('Error getting simple employee detail:', e)
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
