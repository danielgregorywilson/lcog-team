import { WorkflowInstanceRetrieve } from '../../types'

export interface WorkflowStateInterface {
  currentWorkflowInstance: WorkflowInstanceRetrieve
}

const blankWorkflowInstance = {
  pk: -1, workflow: -1
}

const state: WorkflowStateInterface = {
  currentWorkflowInstance: blankWorkflowInstance,
};

export default state;
