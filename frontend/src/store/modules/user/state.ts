export interface EmployeeProfileInterface {
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
  profile: {username: '', email: '', name: '', is_manager: false, is_upper_manager: false}
};

export default state;
