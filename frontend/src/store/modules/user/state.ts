export interface EmployeeProfileInterface {
  employee_pk: number
  username: ''
  email: ''
  name: ''
  is_manager: boolean
  has_manager: boolean
  is_eligible_for_telework_application: boolean
  can_view_seating_charts: boolean
  can_edit_seating_charts: boolean
  is_upper_manager: boolean
  is_hr_manager: boolean
  is_executive_director: boolean
  viewed_security_message: boolean
  prs_can_view: Array<number>
  notes_can_view: Array<number>
  telework_applications_can_view: Array<number>
  time_off_requests_can_view: Array<number>
  next_to_sign_prs: string
}

export interface UserStateInterface {
  status: string;
  profile: EmployeeProfileInterface;
}

const state: UserStateInterface = {
  status: '',
  profile: {employee_pk: -1, username: '', email: '', name: '', is_manager: false, has_manager: false, is_eligible_for_telework_application: false, can_view_seating_charts: false, can_edit_seating_charts: false, is_upper_manager: false, is_hr_manager: false, is_executive_director: false, viewed_security_message: false, prs_can_view: [], notes_can_view: [], telework_applications_can_view: [], time_off_requests_can_view: [], next_to_sign_prs: ''}
};

export default state;
