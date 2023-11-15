import { Url } from 'url'

/////////////////////////////////////////////////////
// Auth Users Structure from Django Rest Framework //
/////////////////////////////////////////////////////

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

///////////////////////////////////////////////////
// Employee Structure from Django Rest Framework //
///////////////////////////////////////////////////

export interface EmployeeRetrieve {
  url: string
  pk: number
  name: string
  user: Url
  username: string
  email: string
  manager: Url
  division: string
  is_manager: boolean
  has_manager: boolean
  is_is_employee: boolean
  is_hr_employee: boolean
  is_sds_hiring_lead: boolean
  is_fiscal_employee: boolean
  is_upper_manager: boolean
  is_hr_manager: boolean
  is_executive_director: boolean
  viewed_security_message: boolean
  is_eligible_for_telework_application: boolean
  can_view_seating_charts: boolean
  can_edit_seating_charts: boolean
  can_view_desk_reservation_reports: boolean
  prs_can_view: Array<number>
  notes_can_view: Array<number>
  time_off_requests_can_view: Array<number>
  telework_applications_can_view: Array<number>
  next_to_sign_prs: string
  email_opt_out_all: boolean
  email_opt_out_timeoff_all: boolean
  email_opt_out_timeoff_weekly: boolean
  email_opt_out_timeoff_daily: boolean
  is_all_workflows_admin: boolean
  admin_of_workflows: Array<number>
  admin_of_processes: Array<number>
  workflow_roles: Array<number>
  can_view_expenses: boolean
  can_view_mow_routes: boolean
  can_manage_mow_stops: boolean
}

export interface SimpleEmployeeRetrieve {
  pk: number
  name: string
  legal_name: string
}

export interface EmployeeEmailRetrieve {
  email: string
}

// For updating employee profile
export interface EmployeeUpdatePartial {
  display_name?: string
  email_opt_out_all: boolean
  email_opt_out_timeoff_all: boolean
  email_opt_out_timeoff_weekly: boolean
  email_opt_out_timeoff_daily: boolean
}

/////////////////////////////////////////////////
// People Structure from Django Rest Framework //
/////////////////////////////////////////////////

export interface Title {
  pk: number
  name: string
}

export interface Unit {
  pk: number
  name: string
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

////////////////////////////////////////////////////////////////
// ViewedSecurityMessage Structure from Django Rest Framework //
////////////////////////////////////////////////////////////////

export interface SecurityMessage {
  content: string
}

export interface ViewedSecurityMessageCreate {
  employee_pk: number
  security_message_pk: number
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
  tags: Array<ResponsibilityTagRetrieve>
  primary_employee_pk?: number
  primary_employee_name?: string
  secondary_employee_pk?: number
  secondary_employee_name?: string
}

export interface ResponsibilityCreate {
  name: string
  description?: string
  link?: string
  tags?: Array<ResponsibilityTagRetrieve>
  primary_employee?: number
  secondary_employee?: number
}

export interface ResponsibilityUpdate {
  pk?: number
  name?: string
  description?: string
  link?: string
  tags?: Array<ResponsibilityTagRetrieve>
  primary_employee?: number
  secondary_employee?: number
}

export interface ResponsibilityNameUpdate extends ResponsibilityUpdate {
  name: string
}

export interface EmployeeResponsibilitiesInterface {
  pk: string
  responsibilities: Array<Responsibility>
}

export interface SimpleResponsibilityTagRetrieve {
  pk: number
  name: string
}

export interface ResponsibilityTagRetrieve {
  pk?: number
  name: string
  responsibilities: Array<Responsibility>
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

export interface GetReservationReportData {
  startDateTime: string
  endDateTime: string
}

export interface GetDeskReservationDataInterface {
  [key: string]: {
    'total_hours': string,
    'days_utilized': number,
    'most_frequent_employee': string
  }
}

export interface GetEmployeeDeskReservationDataInterface {
  [key: string]: {
    'total_hours': string,
    'days_utilized': number,
    'most_frequent_desk': string
  }
}

/////////////////////////////////////////////////////////
// TimeOffRequest Structure from Django Rest Framework //
/////////////////////////////////////////////////////////

export interface TimeOffRequestRetrieve {
  url: Url
  pk: number
  employee_pk: number
  employee_name: string
  manager_pk: number
  start_date: Date
  end_date: Date
  past: boolean
  note: string
  private_note: string
  acknowledged: boolean
  conflicts?: JSON
}

export type TimeOffRequestDates = {from: string; to: string} | string

export interface TimeOffRequestCreate {
  dates: TimeOffRequestDates
  note: string
  privateNote: string
}

export interface TimeOffRequestAcknowledge {
  pk: number
  acknowledged: boolean
}

export interface TimeOffRequestUpdate {
  pk: string
  dates: TimeOffRequestDates
  note: string
  privateNote: string
}

export interface TimeOffRequestUpdatePartial {
  acknowledged: boolean
}

export interface EmployeeConflictingResponsibilities {
  pk: number
  name: string
  responsibility_names: Array<string>
}

///////////////////////////////////////////////////
// Workflow Structure from Django Rest Framework //
///////////////////////////////////////////////////

export type Workflow = {
  pk: number
  name: string
  role: number
  version: number
}

type Process = {
  pk: number
  name: string
  workflow: Workflow
  role: Role
  version: number
}

export type Role = {
  pk: number
  name: string
  description: string
  members: Array<EmployeeRetrieve>
}

export type Action = {
  pk: number
  type: string
  name: string
  description: string
  url: URL
}

export type Step = {
  pk: number
  name: string
  description: string
  process: Process
  role: Role
  next_step: Step
  choices_prompt: string
  next_step_choices: Array<StepChoice>
  workflow_role_pk: number
  process_role_pk: number
  completion_action: Action
  optional_actions: Array<Action>
}

type StepChoice = {
  pk: number
  choice_text: string
  next_step_pk: number
}

export type StepInstance = {
  pk: number
  step: Step
  completed_at: Date
  completed_by: number
  completed_by_name: string
  undo_completion_possible: boolean
}

export type ProcessInstance = {
  pk: number
  process: Process
  step_instances: Array<StepInstance>
  current_step_instance: StepInstance
  started_at: string
  completed_at: string
  percent_complete: number
}

export interface WorkflowInstanceSimple {
  pk: number
  started_at: string
  complete: boolean
  completed_at: string
  percent_complete: number
  status: string | number
  employee_name: string
  title_name: string
  transition_type: string
  transition_date: string
  workflow_role_pk: number
}

export interface WorkflowInstance {
  pk: number
  workflow: Workflow
  process_instances: Array<ProcessInstance>
  transition: EmployeeTransition
  active: boolean
  complete: boolean
  percent_complete: number
  title_name: string
  workflow_role_pk: number
}

export type EmployeeID = 'CLSD' | 'CLID' | ''

interface EmployeeTransitionBase {
  salary_range: number | null
  salary_step: number | null
  cubicle_number: number | null
}

export interface TransitionChange {
  pk: number
  transition: number
  created_by: number
  created_by_name: string
  created_by_initials: string
  date: string
  changes: string
}

export interface EmployeeTransition extends EmployeeTransitionBase {
  pk: number
  type: string
  date_submitted: Date
  submitter_pk: number
  submitter_name: string
  submitter_division: string
  employee_first_name: string
  employee_middle_initial: string
  employee_last_name: string
  employee_preferred_name: string
  employee_number: string
  employee_id: string // TODO This should be EmployeeID
  employee_email: string
  title_pk: number
  title_name: string
  fte: string
  bilingual: boolean
  second_language: string
  manager_pk: number
  manager_name: string
  unit_pk: number
  unit_name: string
  transition_date: string
  lwop: boolean
  lwop_details: string
  preliminary_hire: boolean
  delete_profile: boolean
  office_location: string
  cubicle_number: number | null
  union_affiliation: string
  teleworking: boolean
  computer_type: string
  computer_gl: string
  computer_description: string
  phone_number: string
  desk_phone: boolean
  phone_request: string
  phone_request_data: string
  load_code: string
  cell_phone: boolean
  should_delete: boolean
  reassign_to: string
  gas_pin_needed: boolean
  business_cards: boolean
  prox_card_needed: boolean
  prox_card_returned: boolean
  access_emails_pk: number
  access_emails_name: string
  special_instructions: string
  fiscal_field: string
  assignee: string
  changes: Array<TransitionChange>
}

export interface EmployeeTransitionUpdate extends EmployeeTransitionBase {
  type?: string
  submitter_pk: number
  employee_first_name?: string
  employee_middle_initial?: string
  employee_last_name?: string
  employee_preferred_name?: string
  employee_number?: string
  employee_id?: string // TODO This should be EmployeeID
  employee_email?: string
  title_pk?: number
  fte?: string
  bilingual?: boolean
  second_language?: string
  manager_pk?: number
  unit_pk?: number
  transition_date?: Date
  lwop?: boolean
  lwop_details?: string
  preliminary_hire?: boolean
  delete_profile?: boolean
  office_location?: string
  union_affiliation?: string
  teleworking?: boolean
  computer_type?: string
  computer_gl?: string
  computer_description?: string
  phone_number?: string
  desk_phone?: boolean
  phone_request?: string
  phone_request_data?: string
  load_code?: string
  cell_phone?: boolean
  should_delete?: boolean
  reassign_to?: string
  gas_pin_needed?: boolean
  business_cards?: boolean
  prox_card_needed?: boolean
  prox_card_returned?: boolean
  access_emails_pk?: number
  special_instructions?: string
  fiscal_field?: string
  assignee?: string
}

////////////////////////////////////////////////
// Meals Structure from Django Rest Framework //
////////////////////////////////////////////////

export interface LatLong {
  lat: number
  long: number
}

export interface MealStateInterface {
  stops: Array<Stop>
}

export interface Stop {
  first_name: string
  last_name: string
  address: string
  city: string
  zip_code: number
  latitude: number
  longitude: number
  meal_type: 'hot' | 'cold'
  waitlist: boolean
  phone: string
  phone_notes: string
  notes: string
  route_name: string
  created_at?: Date
  updated_at?: Date
  new?: boolean
}

///////////////
// Utilities //
///////////////

export interface ClientError {
  message: string
  location: string
}
