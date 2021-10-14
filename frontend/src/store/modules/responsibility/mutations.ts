import { ResponsibilityRetrieve } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { ResponsibilityStateInterface } from './state'


const mutation: MutationTree<ResponsibilityStateInterface> = {
  setAllResponsibilities: (state, resp: {data: Array<ResponsibilityRetrieve>}) => {
    Vue.set(state, 'allResponsibilities', resp.data)
  },
  setOrphanedResponsibilities: (state, resp: {data: Array<ResponsibilityRetrieve>}) => {
    Vue.set(state, 'orphanedResponsibilities', resp.data)
  },
  setEmployeePrimaryResponsibilities: (state, resp: {employeePk: number, responsibilities: {data: Array<ResponsibilityRetrieve>}}) => {
    let employeeResponsibilities = state.employeePrimaryResponsibilities
    let thisEmployeeResponsibilities = employeeResponsibilities.filter(employeeObj => employeeObj.pk == resp.employeePk)[0]
    if (thisEmployeeResponsibilities) {
      debugger
    } else {
      let retrievedObj = resp.responsibilities.data
      for (let obj of retrievedObj) {
        debugger
      }
      retrievedObj.forEach(obj => {
        debugger
      })
      const employeeResponsibilitiesObj = {pk: resp.employeePk, responsibilities: resp.responsibilities.data}
      employeeResponsibilities.push(employeeResponsibilitiesObj)
    }
    Vue.set(state, 'employeePrimaryResponsibilities', {...state.employeePrimaryResponsibilities, foobar: 123})
    // Vue.set(state, 'employeePrimaryResponsibilities', ...state.employeePrimaryResponsibilities, ...{resp.employeePk: {resp.responsibilities.data}})
    // Vue.set(state, 'employeePrimaryResponsibilities', resp.employeePk, resp.responsibilities.data)
  },
  // setUserSecondaryResponsibilities: (state, resp: {data: Array<ResponsibilityRetrieve>}) => {
  //   Vue.set(state, 'allResponsibilities', resp.data)
  // },
  authLogout: (state) => {
    // Clean up state
    state.allResponsibilities = []
    state.orphanedResponsibilities = []
    state.employeePrimaryResponsibilities = []
    state.employeeSecondaryResponsibilities = []
  }
};

export default mutation;
