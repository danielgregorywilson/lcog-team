import { SimpleEmployeeRetrieve, Unit } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { PeopleStateInterface } from '../../types'


const mutation: MutationTree<PeopleStateInterface> = {
  setSimpleEmployeeList: (state, resp: {data: Array<SimpleEmployeeRetrieve>}) => {
    Vue.set(state, 'simpleEmployeeList', resp.data)
  },
  setSimpleEmployeeDetail: (state, resp: {data: SimpleEmployeeRetrieve}) => {
    Vue.set(state, 'simpleEmployeeDetail', resp.data)
  },
  setUnitList: (state, resp: {data: Array<Unit>}) => {
    Vue.set(state, 'unitList', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.simpleEmployeeList = []
    // TODO: state.simpleEmployeeDetail =
    state.unitList = [] 
  }
};

export default mutation;
