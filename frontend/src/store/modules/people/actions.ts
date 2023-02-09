import { ActionTree } from 'vuex'
import { StateInterface } from '../../index'
import { PeopleStateInterface } from '../../types'
import axios from 'axios'

function getApiUrl(): string {
  if (process.env.API_URL) {
    return process.env.API_URL
  } else {
    return ''
  }
}

const actions: ActionTree<PeopleStateInterface, StateInterface> = {
  getSimpleEmployeeList: ({ commit }) => {
    axios({ url: `${ getApiUrl() }api/v1/employee/simple_list`}) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setSimpleEmployeeList', resp)
      })
      .catch(e => {
        console.error('Error getting simple employee list:', e)
      })
  },
  getSimpleEmployeeDetail: ({ commit }, data: {pk: number}) => {
    axios({ url: `${ getApiUrl() }api/v1/employee/${ data.pk }/simple_detail`}) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setSimpleEmployeeDetail', resp)
      })
      .catch(e => {
        console.error('Error getting simple employee detail:', e)
      })
  },
  getUnitList: ({ commit }) => {
    axios({ url: `${ getApiUrl() }api/v1/unit`}) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setUnitList', resp)
      })
      .catch(e => {
        console.error('Error getting unit list:', e)
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
