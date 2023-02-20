import { EmployeeTransition, Role, Workflow, WorkflowInstance } from '../../types'

export interface WorkflowStateInterface {
  currentWorkflowInstance: WorkflowInstance
  currentEmployeeTransition: EmployeeTransition
  workflowsActionRequired: Array<WorkflowInstance>
  workflowsComplete: Array<WorkflowInstance>
  workflowsIncomplete: Array<WorkflowInstance>
  allWorkflows: Array<WorkflowInstance>
}

const blankRole: Role = {
  pk: -1, name: '', description: '', members: []
}

const blankWorkflow: Workflow = {
  pk: -1, name: '', version: -1, role: blankRole
}

const blankEmployeeTransition: EmployeeTransition = {
  pk: -1, type: '', date_submitted: new Date(), submitter_name: '',
  employee_first_name: '', employee_middle_initial: '', employee_last_name: '',
  employee_preferred_name: '', employee_number: '', employee_id: 'CLSD',
  employee_email: '', title: '', fte: '', salary_range: null, salary_step: null,
  bilingual: false, manager_pk: -1, manager_name: '', unit_pk: -1,
  unit_name: '', transition_date: new Date(), preliminary_hire: false,
  delete_profile: false, office_location: '', cubicle_number: null,
  union_affiliation: '', teleworking: false, desk_phone: false,
  current_phone: '', phone_request: '', phone_request_data: '', load_code: '',
  should_delete: false, reassign_to: '', business_cards: false,
  prox_card_needed: false, prox_card_returned: false, access_emails_pk: -1,
  access_emails_name: '', special_instructions: ''
}

// const blankEmployeeTransition = {
//   pk: -1, type: '', date_submitted: new Date(), submitter_name: '',
//   employee_first_name: '', employee_middle_initial: '', employee_last_name: '',
//   employee_preferred_name: '', employee_number: '', employee_id: '',
// }

export const blankWorkflowInstance: WorkflowInstance = {
  pk: -1, workflow: blankWorkflow, started_at: '', completed_at: '',
  process_instances: [], transition: blankEmployeeTransition, title: '',
  percent_complete: ''
}

const state: WorkflowStateInterface = {
  currentWorkflowInstance: blankWorkflowInstance, currentEmployeeTransition: blankEmployeeTransition,
  workflowsActionRequired: [], workflowsComplete: [], workflowsIncomplete: [], allWorkflows: []
};

export default state;
