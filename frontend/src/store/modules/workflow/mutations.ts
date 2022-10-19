import Vue from 'vue'

import { MutationTree } from 'vuex'
import { WorkflowStateInterface } from './state'
import { WorkflowInstanceRetrieve } from '../../types'


const mutation: MutationTree<WorkflowStateInterface> = {
  setCurrentWorkflowInstance: (state, resp: {data: Array<WorkflowInstanceRetrieve>}) => {
    Vue.set(state, 'currentWorkflowInstance', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.currentWorkflowInstance = {pk: -1, workflow: -1}
  }
};

export default mutation;
