import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { WorkflowStateInterface } from './state';

const getters: GetterTree<WorkflowStateInterface, StateInterface> = {
  currentWorkflowInstance: state => state.currentWorkflowInstance,
  currentEmployeeTransition: state => state.currentWorkflowInstance.transition,
  workflowsActionRequired: state => state.workflowsActionRequired,
  workflowsComplete: state => state.workflowsComplete,
  workflowsIncomplete: state => state.workflowsIncomplete,
  allWorkflows: state => state.allWorkflows,
  processInstanceCurrentStepPks: state => {
    const d = {}
    state.currentWorkflowInstance.process_instances.forEach(pi => {
      if (pi.current_step_instance) {
        d[pi.pk] = pi.current_step_instance.pk  
      } else {
        d[pi.pk] = -1
      }
    })
    return d
  }
};

export default getters;
