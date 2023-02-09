import { EmployeeTransition, WorkflowInstance } from '../../types'

export interface WorkflowStateInterface {
  currentWorkflowInstance: WorkflowInstance
  currentEmployeeTransition: EmployeeTransition
  workflowsActionRequired: Array<WorkflowInstance>
  workflowsComplete: Array<WorkflowInstance>
  workflowsIncomplete: Array<WorkflowInstance>
  allWorkflows: Array<WorkflowInstance>
}

const blankRole = {
  pk: -1, name: '', description: '', members: []
}

const blankWorkflow = {
  pk: -1, name: '', version: -1, role: blankRole
}

const blankEmployeeTransition = {
  pk: -1
}

export const blankWorkflowInstance = {
  pk: -1, workflow: blankWorkflow, transition: blankEmployeeTransition, process_instances: [], started_at: '', completed_at: ''
}

const state: WorkflowStateInterface = {
  currentWorkflowInstance: blankWorkflowInstance, currentEmployeeTransition: blankEmployeeTransition,
  workflowsActionRequired: [], workflowsComplete: [], workflowsIncomplete: [], allWorkflows: []
};

export default state;
