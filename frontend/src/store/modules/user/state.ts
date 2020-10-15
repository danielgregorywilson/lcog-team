export interface EmployeeProfileInterface {
  employee_pk: number
  username: ''
  email: ''
  name: ''
  is_manager: boolean
  is_upper_manager: boolean
}

export interface UserStateInterface {
  status: string;
  profile: EmployeeProfileInterface;
}

const state: UserStateInterface = {
  status: '',
  profile: {employee_pk: -1, username: '', email: '', name: '', is_manager: false, is_upper_manager: false}
};

export default state;
