import { AxiosResponse } from 'axios'
import { Url } from 'url'

/////////////////////////////////////////////////////
// Auth Users Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface AxiosAuthResponse extends AxiosResponse {
  data: {
    token: string
  }
}

export interface UserRetrieve {
  url: Url
  username: string
  email: string
  name: string
  firstName?: string
  lastName?: string
  is_staff: boolean
  is_manager: boolean
  is_upper_manager: boolean
  can_view_desk_reservation_reports: boolean
}

export interface AxiosUserRetrieveOneServerResponse {
  data: UserRetrieve
}

///////////////////////////////////////////////////
// Employee Structure from Django Rest Framework //
///////////////////////////////////////////////////

export interface EmployeeRetrieve {
  url: string
  pk: number
  name: string
  user: Url
  email: string
  manager: Url
  is_manager: boolean
  has_manager: boolean
  is_upper_manager: boolean
  is_hr_manager: boolean
  is_executive_director: boolean
  is_eligible_for_telework_application: boolean
  can_view_seating_charts: boolean
  can_edit_seating_charts: boolean
  prs_can_view: Array<number>
  notes_can_view: Array<number>
  time_off_requests_can_view: Array<number>
  telework_applications_can_view: Array<number>
  next_to_sign_prs: string
  email_opt_out_all: boolean
  email_opt_out_timeoff_all: boolean
  email_opt_out_timeoff_weekly: boolean
  email_opt_out_timeoff_daily: boolean
  workflow_roles: Array<number>
}

export interface SimpleEmployeeRetrieve {
  pk: number
  name: string
}

// For updating employee profile
export interface EmployeeUpdatePartial {
  display_name?: string
  email_opt_out_all: boolean
  email_opt_out_timeoff_all: boolean
  email_opt_out_timeoff_weekly: boolean
  email_opt_out_timeoff_daily: boolean
}

export interface AxiosEmployeeRetrieveOneServerResponse {
  data: EmployeeRetrieve
}

export interface AxiosEmployeeRetrieveManyServerResponse {
  data: {
    results: Array<EmployeeRetrieve>
  }
}

////////////////////////////////////////////////////////////
// PerformanceReview Structure from Django Rest Framework //
////////////////////////////////////////////////////////////

export interface PerformanceReviewRetrieve {
  url: Url
  pk: number
  employee_pk: number
  employee_name: string
  employee_division: string
  employee_unit_or_program: string
  employee_job_title: string
  manager_pk: number
  manager_name: string
  days_until_review: number
  status: string
  period_start_date: Date
  period_end_date: Date
  effective_date: Date
  evaluation_type: string
  probationary_evaluation_type: string
  step_increase: string
  top_step_bonus: string
  action_other: string

  factor_job_knowledge: string
  factor_work_quality: string
  factor_work_quantity: string
  factor_work_habits: string
  factor_analysis: string
  factor_initiative: string
  factor_interpersonal: string
  factor_communication: string
  factor_dependability: string
  factor_professionalism: string
  factor_management: string
  factor_supervision: string
  evaluation_successes: string
  evaluation_opportunities: string
  evaluation_goals_manager: string
  evaluation_comments_employee: string
  
  position_description_link: string
  description_reviewed_employee: boolean
  signed_position_description: string
  all_required_signatures: Array<[string, string, string]>
}

export interface AxiosPerformanceReviewRetrieveOneServerResponse {
  data: PerformanceReviewRetrieve
}

export interface AxiosPerformanceReviewRetrieveManyServerResponse {
  data: {
    results: Array<PerformanceReviewRetrieve>
  }
}

export interface PerformanceReviewCreate {
  url: Url
  pk: number
  employee_name: string
  days_until_review: number
  status: string
}

export interface PerformanceReviewUpdate {
  evaluation_type: string
  probationary_evaluation_type: string
  step_increase: string
  top_step_bonus: string
  action_other: string
  factor_job_knowledge: string
  factor_work_quality: string
  factor_work_quantity: string
  factor_work_habits: string
  factor_analysis: string
  factor_initiative: string
  factor_interpersonal: string
  factor_communication: string
  factor_dependability: string
  factor_professionalism: string
  factor_management: string
  factor_supervision: string
  evaluation_successes: string
  evaluation_opportunities: string
  evaluation_goals_manager: string
  evaluation_comments_employee: string
  description_reviewed_employee: boolean
}

export interface PerformanceReviewUpdatePartial {
  evaluation_type?: string
  probationary_evaluation_type?: string
  step_increase?: string
  top_step_bonus?: string
  action_other?: string
  factor_job_knowledge?: string
  factor_work_quality?: string
  factor_work_quantity?: string
  factor_work_habits?: string
  factor_analysis?: string
  factor_initiative?: string
  factor_interpersonal?: string
  factor_communication?: string
  factor_dependability?: string
  factor_professionalism?: string
  factor_management?: string
  factor_supervision?: string
  evaluation_successes?: string
  evaluation_opportunities?: string
  evaluation_goals_manager?: string
  evaluation_comments_employee?: string
  description_reviewed_employee?: boolean
}

export interface AxiosPerformanceReviewUpdateServerResponse {
  data: PerformanceReviewRetrieve
}

export interface AxiosPerformanceReviewSignServerResponse {
  data: {
    signatures: Array<[string, string, string]>
  }
}

export interface SignedPositionDescriptionUpload {
  pk: string
  file: File
}

export interface FileUploadDescriptionUploadServerResponse {
  data: string
  status: number
  statusText: string
}


/////////////////////////////////////////////////////
// Signature Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface SignatureCreate {
  review_pk: number
  employee_pk: number
}

export interface SignatureRetrieve {
  url: Url
  pk: number
  review: Url
  employee: Url
  date: Date
}

// export interface AxiosReviewNoteRetrieveOneServerResponse {
//   data: ReviewNoteRetrieve
// }

// export interface AxiosManagerReviewNotesForEmployeeServerResponse {
//   data: Array<ReviewNoteRetrieve>
// }

// export interface AxiosReviewNoteRetrieveManyServerResponse {
//   data: {
//     results: Array<ReviewNoteRetrieve>
//   }
// }

// export interface AxiosReviewNoteUpdateServerResponse {
//   data: ReviewNoteRetrieve
// }


/////////////////////////////////////////////////////
// ReviewNote Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface ReviewNoteCreate {
  employee_pk: number
  note: string
}

export interface ReviewNoteRetrieve {
  url: Url
  pk: number
  employee_pk: number
  employee_name: string
  date: Date
  note: string
}

export interface ReviewNoteUpdate {
  employee_pk?: number
  note?: string
}

export interface AxiosReviewNoteRetrieveOneServerResponse {
  data: ReviewNoteRetrieve
}

export interface AxiosManagerReviewNotesForEmployeeServerResponse {
  data: Array<ReviewNoteRetrieve>
}

export interface AxiosReviewNoteRetrieveManyServerResponse {
  data: {
    results: Array<ReviewNoteRetrieve>
  }
}

export interface AxiosReviewNoteUpdateServerResponse {
  data: ReviewNoteRetrieve
}


////////////////////////////////////////////////////////////////
// ViewedSecurityMessage Structure from Django Rest Framework //
////////////////////////////////////////////////////////////////

export interface ViewedSecurityMessageCreate {
  employee_pk: number
}

export interface ViewedSecurityMessageRetrieve {
  url: Url
  pk: number
  employee_pk: number
  security_message_pk: number
  datetime: string
}


//////////////////////////////////////////////////////////////
// TeleworkApplication Structure from Django Rest Framework //
//////////////////////////////////////////////////////////////

export interface TeleworkApplicationRetrieve {
  url: Url
  pk: number
  employee_pk: number
  employee_name: string
  manager_pk: number
  manager_name: string
  program_manager_pk: number
  program_manager_name: string
  status: string
  approval_date: Date
  date: Date
  program_manager_approve: string
  hours_onsite: string
  telework_location: string
  hours_working: string
  duties: string
  communication_when: string
  communication_time: string
  communication_how: string
  equipment_provided_phone: boolean
  equipment_provided_laptop: boolean
  equipment_provided_desktop: boolean
  equipment_provided_monitor: boolean
  equipment_provided_access: boolean
  equipment_provided_other: boolean
  equipment_provided_other_value: string
  workspace_checklist_1: string
  workspace_checklist_2: string
  workspace_checklist_3: string
  workspace_checklist_4: string
  workspace_checklist_5: string
  workspace_checklist_6: string
  workspace_checklist_7: string
  workspace_checklist_8: string
  workspace_checklist_9: string
  workspace_checklist_10: string
  workspace_checklist_11: string
  workspace_checklist_12: string
  emergency_checklist_1: string
  emergency_checklist_2: string
  emergency_checklist_3: string
  ergonomics_checklist_1: string
  ergonomics_checklist_2: string
  ergonomics_checklist_3: string
  ergonomics_checklist_4: string
  ergonomics_checklist_5: string
  teleworker_comments: string
  manager_comments: string
  dependent_care_checklist_1: string
  dependent_care_documentation: string
  
  program_manager_signature_0: [number, string, string, string, number, boolean]
  employee_signature_0: [number, string, string, string, number, boolean]
  employee_signature_1: [number, string, string, string, number, boolean]
  manager_signature: [number, string, string, string, number, boolean]
  program_manager_signature_1: [number, string, string, string, number, boolean]
  division_director_signature: [number, string, string, string, number, boolean]

  
  // employee_division: string
  // employee_unit_or_program: string
  // employee_job_title: string
  // manager_pk: number
  
  // days_until_review: number
  // status: string
  // period_start_date: Date
  // period_end_date: Date
  // effective_date: Date
  // evaluation_type: string
  // probationary_evaluation_type: string
  // step_increase: string
  // top_step_bonus: string
  // action_other: string

  // factor_job_knowledge: string
  // factor_work_quality: string
  // factor_work_quantity: string
  // factor_work_habits: string
  // factor_analysis: string
  // factor_initiative: string
  // factor_interpersonal: string
  // factor_communication: string
  // factor_dependability: string
  // factor_professionalism: string
  // factor_management: string
  // factor_supervision: string
  // evaluation_successes: string
  // evaluation_opportunities: string
  // evaluation_goals_manager: string
  // evaluation_comments_employee: string
  
  // position_description_link: string
  // description_reviewed_employee: boolean
  // signed_position_description: string
  // all_required_signatures: Array<[string, string, string]>
}

export interface AxiosTeleworkApplicationRetrieveOneServerResponse {
  data: TeleworkApplicationRetrieve
}

export interface TeleworkApplicationCreate {
  url: Url
  pk: number
  employee_name: string
  days_until_review: number
  status: string
}

export interface TeleworkApplicationUpdate {
  date: string
  program_manager_approve: string
  hours_onsite: string
  telework_location: string
  hours_working: string
  duties: string
  communication_when: string
  communication_time: string
  communication_how: string
  equipment_provided_phone: boolean
  equipment_provided_laptop: boolean
  equipment_provided_desktop: boolean
  equipment_provided_monitor: boolean
  equipment_provided_access: boolean
  equipment_provided_other: boolean
  equipment_provided_other_value: string
  workspace_checklist_1: string
  workspace_checklist_2: string
  workspace_checklist_3: string
  workspace_checklist_4: string
  workspace_checklist_5: string
  workspace_checklist_6: string
  workspace_checklist_7: string
  workspace_checklist_8: string
  workspace_checklist_9: string
  workspace_checklist_10: string
  workspace_checklist_11: string
  workspace_checklist_12: string
  emergency_checklist_1: string
  emergency_checklist_2: string
  emergency_checklist_3: string
  ergonomics_checklist_1: string
  ergonomics_checklist_2: string
  ergonomics_checklist_3: string
  ergonomics_checklist_4: string
  ergonomics_checklist_5: string
  teleworker_comments: string
  manager_comments: string
  dependent_care_checklist_1: string
  // dependent_care_documentation: ??
}

export interface TeleworkApplicationUpdatePartial {
  evaluation_type?: string
  probationary_evaluation_type?: string
  step_increase?: string
  top_step_bonus?: string
  action_other?: string
  factor_job_knowledge?: string
  factor_work_quality?: string
  factor_work_quantity?: string
  factor_work_habits?: string
  factor_analysis?: string
  factor_initiative?: string
  factor_interpersonal?: string
  factor_communication?: string
  factor_dependability?: string
  factor_professionalism?: string
  factor_management?: string
  factor_supervision?: string
  evaluation_successes?: string
  evaluation_opportunities?: string
  evaluation_goals_manager?: string
  evaluation_comments_employee?: string
  description_reviewed_employee?: boolean
}

export interface AxiosTeleworkApplicationUpdateServerResponse {
  data: TeleworkApplicationRetrieve
}

// export interface AxiosPerformanceReviewSignServerResponse {
//   data: {
//     signatures: Array<[string, string, string]>
//   }
// }

// export interface SignedPositionDescriptionUpload {
//   pk: string
//   file: File
// }

// export interface SignedPositionDescriptionUploadServerResponse {
//   data: string
//   status: number
//   statusText: string
// }


////////////////////////////////////////////////////////////
// TeleworkSignature Structure from Django Rest Framework //
////////////////////////////////////////////////////////////

export interface TeleworkSignatureCreate {
  application_pk: number
  employee_pk: number
  index: number
}

export interface TeleworkSignatureRetrieve {
  url: Url
  pk: number
  application: Url
  employee: Url
  index: number
  date: Date
}


/////////////////////////////////////////////////////////
// Responsibility Structure from Django Rest Framework //
/////////////////////////////////////////////////////////

export interface Responsibility {
  pk: number
  name: string
  description: string
  link: string
  tags: Array<ResponsibilityTag>
  primary_employee_pk?: number
  primary_employee_name?: string
  secondary_employee_pk?: number
  secondary_employee_name?: string
}

export interface ResponsibilityCreate {
  name: string
  description?: string
  link?: string
  tags?: Array<ResponsibilityTag>
  primary_employee?: number
  secondary_employee?: number
}

export interface ResponsibilityUpdate {
  pk?: number
  name?: string
  description?: string
  link?: string
  tags?: Array<ResponsibilityTag>
  primary_employee?: number
  secondary_employee?: number
}

export interface ResponsibilityNameUpdate extends ResponsibilityUpdate {
  name: string
}

export interface AxiosResponsibilityUpdateServerResponse {
  data: Responsibility
}

export interface ResponsibilityStateInterface {
  allResponsibilities: { results: Array<Responsibility> }
  orphanedResponsibilities: Array<Responsibility>
  employeePrimaryResponsibilities: Array<EmployeeResponsibilitiesInterface>
  employeeSecondaryResponsibilities: Array<EmployeeResponsibilitiesInterface>
  tagWithResponsibilities: Array<EmployeeResponsibilitiesInterface>
  allTags: { results: Array<ResponsibilityTag> }
  simpleEmployeeList: Array<SimpleEmployeeRetrieve>
  simpleEmployeeDetail: SimpleEmployeeRetrieve
  simpleTagList: Array<SimpleResponsibilityTagRetrieve>
}

export interface EmployeeResponsibilitiesInterface {
  pk: number
  responsibilities: Array<Responsibility>
}

export interface SimpleResponsibilityTagRetrieve {
  pk: number
  name: string
}

export interface ResponsibilityTag {
  pk?: number
  name: string
  responsibilities?: Array<string>
}

export interface ResponsibilityTagCreate {
  name: string
}

export interface ResponsibilityTagUpdate {
  pk?: number
  name?: string
}


//////////////////////////////////////////////////////////
// DeskReservation Structure from Django Rest Framework //
//////////////////////////////////////////////////////////

export interface Desk {
  pk: number
  building: string
  floor: string
  number: string
  letter?: string
  active: boolean
  lead: boolean
  ergonomic: boolean
  held_today: boolean
}

export interface DeskReservation {
  pk: number
  employee_pk: number
  employee_name: string
  desk_building: string
  desk_floor: string
  desk_number: string
  check_in: string
  check_out: string
  created?: boolean
  desk_held?: boolean
}

export interface DeskReservationCreate {
  employee_pk: number
  building: string
  floor: string
  desk_number: string
}

export interface AxiosDeskReservationCreateServerResponse {
  data: DeskReservation
}

export interface GetReservationReportData {
  startDateTime: string
  endDateTime: string
}

export interface AxiosGetDeskReservationReportDataServerResponse {
  data: GetDeskReservationDataInterface
}

export interface GetDeskReservationDataInterface {
  [key: string]: {
    'total_hours': string,
    'days_utilized': number,
    'most_frequent_employee': string
  }
}

export interface AxiosGetEmployeeDeskReservationReportDataServerResponse {
  data: GetEmployeeDeskReservationDataInterface
}

export interface GetEmployeeDeskReservationDataInterface {
  [key: string]: {
    'total_hours': string,
    'days_utilized': number,
    'most_frequent_desk': string
  }
}

export interface DeskReservationStateInterface {
  allDesks: { results: Array<Desk> }
  allDeskReservations: { results: Array<DeskReservation> }
}


/////////////////////////////////////////////////////////
// TimeOffRequest Structure from Django Rest Framework //
/////////////////////////////////////////////////////////

export type TimeOffRequestDates = {from: string; to: string} | string

export interface TimeOffRequestCreate {
  employee_pk: number
  dates: TimeOffRequestDates
  note: string
  privateNote: string
}

export interface TimeOffRequestAcknowledge {
  pk: number
  acknowledge: boolean
}

export interface TimeOffRequestRetrieve {
  url: Url
  pk: number
  employee_pk: number
  employee_name: string
  manager_pk: number
  start_date: Date
  end_date: Date
  note: string
  private_note: string
  acknowledged: boolean
  conflicts?: JSON
}

export interface TimeOffRequestUpdate {
  dates: TimeOffRequestDates
  note: string
  privateNote: string
}

export interface TimeOffRequestUpdatePartial {
  acknowledged: boolean
}

export interface AxiosTimeOffRequestRetrieveOneServerResponse {
  data: TimeOffRequestRetrieve
}


///////////////////////////////////////////////////
// Workflow Structure from Django Rest Framework //
///////////////////////////////////////////////////

type Workflow = {
  pk: number
  name: string
  role: Role
  version: number
}

type Process = {
  pk: number
  name: string
  workflow: Workflow
  role: Role
  version: number
}

type Role = {
  pk: number
  name: string
  description: string
  members: Array<EmployeeRetrieve>
}

export type Step = {
  pk: number
  name: string
  description: string
  process: Process
  role: Role
  choices_prompt: string
  next_step_choices: Array<StepChoice>
  workflow_role_pk: number
  process_role_pk: number
}

type StepChoice = {
  pk: number
  choice_text: string
  next_step_pk: number
}

type StepInstance = {
  pk: number
  step: Step
  completed_at: string
}

export type ProcessInstance = {
  pk: number
  process: Process
  step_instances: Array<StepInstance>
  current_step_instance: StepInstance
  started_at: string
  completed_at: string
}

export interface WorkflowInstanceRetrieve {
  pk: number
  workflow: Workflow
  started_at: string
  completed_at: string
  process_instances: Array<ProcessInstance>
}

export interface AxiosTimeOffRequestRetrieveOneServerResponse {
  data: TimeOffRequestRetrieve
}


/////////////
// Getters //
/////////////

export interface VuexStoreGetters {
  'authModule/isAuthenticated': boolean,
  'userModule/getEmployeeProfile': EmployeeRetrieve,

  // Desk Reservation
  'deskReservationModule/allDesks': {
    results: Array<Desk>
  },
  'deskReservationModule/allDeskReservations': {
    results: Array<DeskReservation>
  },

  // Time Off
  'timeOffModule/teamTimeOffRequests': {
    results: Array<TimeOffRequestRetrieve>
  },
  'timeOffModule/myTimeOffRequests': {
    results: Array<TimeOffRequestRetrieve>
  },
  'timeOffModule/managedTimeOffRequests': {
    results: Array<TimeOffRequestRetrieve>
  },
  'timeOffModule/conflictingTimeOffRequests': Array<TimeOffRequestRetrieve>,

  // Responsibilities
  'responsibilityModule/simpleEmployeeList': Array<SimpleEmployeeRetrieve>,
  'responsibilityModule/simpleEmployeeDetail': SimpleEmployeeRetrieve,
  'responsibilityModule/allResponsibilities': {
    results: Array<Responsibility>
  },
  'responsibilityModule/orphanedResponsibilities': {
    results: Array<Responsibility>
  },
  'responsibilityModule/employeePrimaryResponsibilities': Array<EmployeeResponsibilitiesInterface>,
  'responsibilityModule/employeeSecondaryResponsibilities': Array<EmployeeResponsibilitiesInterface>
  'responsibilityModule/tagWithResponsibilities': ResponsibilityTag
  'responsibilityModule/allTags': {
    results: Array<SimpleResponsibilityTagRetrieve>
  },
  'responsibilityModule/simpleTagList': Array<SimpleResponsibilityTagRetrieve>,

  // Workflows
  'workflowModule/currentWorkflowInstance': WorkflowInstanceRetrieve
}