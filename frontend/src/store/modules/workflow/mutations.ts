import Vue from 'vue'

import { MutationTree } from 'vuex'
import { blankWorkflowInstance, WorkflowStateInterface } from './state'
import { EmployeeTransition, WorkflowInstance } from '../../types'


const mutation: MutationTree<WorkflowStateInterface> = {
  setCurrentWorkflowInstance: (state, resp: {data: Array<WorkflowInstance>}) => {
    Vue.set(state, 'currentWorkflowInstance', resp.data)
  },
  setAllWorkflows: (state, resp: {data: Array<WorkflowInstance>}) => {
    Vue.set(state, 'allWorkflows', resp.data)
  },
  setWorkflowsActionRequired: (state, resp: {data: Array<WorkflowInstance>}) => {
    Vue.set(state, 'workflowsActionRequired', resp.data)
  },
  setWorkflowsComplete: (state, resp: {data: Array<WorkflowInstance>}) => {
    Vue.set(state, 'workflowsComplete', resp.data)
  },
  setWorkflowsIncomplete: (state, resp: {data: Array<WorkflowInstance>}) => {
    Vue.set(state, 'workflowsIncomplete', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.currentWorkflowInstance = blankWorkflowInstance
  }
};

export default mutation;
