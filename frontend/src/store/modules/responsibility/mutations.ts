import { Responsibility, ResponsibilityNameUpdate, ResponsibilityTag, SimpleEmployeeRetrieve } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { ResponsibilityStateInterface } from '../../types'


const mutation: MutationTree<ResponsibilityStateInterface> = {
  setAllResponsibilities: (state, resp: {data: Array<Responsibility>}) => {
    Vue.set(state, 'allResponsibilities', resp.data)
  },
  setOrphanedResponsibilities: (state, resp: {data: Array<Responsibility>}) => {
    Vue.set(state, 'orphanedResponsibilities', resp.data)
  },
  setEmployeePrimaryResponsibilities: (state, resp: {employeePk: number, responsibilities: {data: {results: Array<Responsibility>}}}) => {
    const employeeResponsibilities = state.employeePrimaryResponsibilities
    const thisEmployeeResponsibilities = employeeResponsibilities.filter(employeeObj => employeeObj.pk == resp.employeePk)[0]
    if (thisEmployeeResponsibilities) {
      thisEmployeeResponsibilities.responsibilities = resp.responsibilities.data.results
    } else {
      const employeeResponsibilitiesObj = {pk: resp.employeePk, responsibilities: resp.responsibilities.data.results}
      employeeResponsibilities.push(employeeResponsibilitiesObj)
    }
    Vue.set(state, 'employeePrimaryResponsibilities', employeeResponsibilities)
  },
  setEmployeeSecondaryResponsibilities: (state, resp: {employeePk: number, responsibilities: {data: {results: Array<Responsibility>}}}) => {
    const employeeResponsibilities = state.employeeSecondaryResponsibilities
    const thisEmployeeResponsibilities = employeeResponsibilities.filter(employeeObj => employeeObj.pk == resp.employeePk)[0]
    if (thisEmployeeResponsibilities) {
      thisEmployeeResponsibilities.responsibilities = resp.responsibilities.data.results
    } else {
      const employeeResponsibilitiesObj = {pk: resp.employeePk, responsibilities: resp.responsibilities.data.results}
      employeeResponsibilities.push(employeeResponsibilitiesObj)
    }
    Vue.set(state, 'employeeSecondaryResponsibilities', employeeResponsibilities)
  },
  updateResponsibilityName: (state, data: ResponsibilityNameUpdate) => {
    state.allResponsibilities.results.filter(r => r.pk == data.pk)[0].name = data.name
  },
  setAllTags: (state, resp: {data: Array<ResponsibilityTag>}) => {
    Vue.set(state, 'allTags', resp.data)
  },
  setSimpleEmployeeList: (state, resp: {data: Array<SimpleEmployeeRetrieve>}) => {
    Vue.set(state, 'simpleEmployeeList', resp.data)
  },
  setSimpleEmployeeDetail: (state, resp: {data: SimpleEmployeeRetrieve}) => {
    Vue.set(state, 'simpleEmployeeDetail', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.allResponsibilities = { results: [] }
    state.orphanedResponsibilities = []
    state.employeePrimaryResponsibilities = []
    state.employeeSecondaryResponsibilities = []
    state.allTags = { results: [] }
    state.simpleEmployeeList = []
  }
};

export default mutation;
