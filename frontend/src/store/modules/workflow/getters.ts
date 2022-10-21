import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { WorkflowStateInterface } from './state';

const getters: GetterTree<WorkflowStateInterface, StateInterface> = {
  currentWorkflowInstance: state => state.currentWorkflowInstance
};

export default getters;
