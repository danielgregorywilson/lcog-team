import { WorkflowInstance } from '../../types'

export interface WorkflowStateInterface {
  currentWorkflowInstance: WorkflowInstance
  workflowsActionRequired: Array<WorkflowInstance>
  workflowsComplete: Array<WorkflowInstance>
  workflowsIncomplete: Array<WorkflowInstance>
  allWorkflows: Array<WorkflowInstance>
}

const blankWorkflowInstance = {
  pk: -1, workflow: -1, process_instances: [], started_at: '', completed_at: ''
}

const state: WorkflowStateInterface = {
  currentWorkflowInstance: blankWorkflowInstance, workflowsActionRequired: [],
  workflowsComplete: [], workflowsIncomplete: [], allWorkflows: []
};

export default state;
