import Vue from 'vue'

import { MutationTree } from 'vuex'
import { WorkflowStateInterface } from './state'
import { WorkflowInstance } from '../../types'


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
    state.currentWorkflowInstance = {pk: -1, workflow: -1, process_instances: [], started_at: '', completed_at: ''}
  }
};

export default mutation;
