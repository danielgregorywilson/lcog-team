import { WorkflowInstanceRetrieve } from '../../types'

export interface WorkflowStateInterface {
  currentWorkflowInstance: WorkflowInstanceRetrieve
  workflowsActionRequired: Array<WorkflowInstanceRetrieve>
  workflowsComplete: Array<WorkflowInstanceRetrieve>
  workflowsIncomplete: Array<WorkflowInstanceRetrieve>
  allWorkflows: Array<WorkflowInstanceRetrieve>
}

const blankWorkflowInstance = {
  pk: -1, workflow: -1, process_instances: []
}

const state: WorkflowStateInterface = {
  currentWorkflowInstance: blankWorkflowInstance, workflowsActionRequired: [],
  workflowsComplete: [], workflowsIncomplete: [], allWorkflows: []
};

export default state;
