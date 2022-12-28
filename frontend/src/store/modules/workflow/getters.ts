import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { WorkflowStateInterface } from './state';

const getters: GetterTree<WorkflowStateInterface, StateInterface> = {
  currentWorkflowInstance: state => state.currentWorkflowInstance,
  workflowsActionRequired: state => state.workflowsActionRequired,
  workflowsComplete: state => state.workflowsComplete,
  workflowsIncomplete: state => state.workflowsIncomplete,
  allWorkflows: state => state.allWorkflows,
};

export default getters;
