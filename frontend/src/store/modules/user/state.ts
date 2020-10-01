export interface EmployeeProfileInterface {
  username: ''
  email: ''
  name: ''
  is_manager: boolean
  is_upper_manager: boolean
}

interface ReviewNoteInterface {

}

export interface UserStateInterface {
  status: string;
  profile: EmployeeProfileInterface;
  allReviewNotes: Array<ReviewNoteInterface>
}

const state: UserStateInterface = {
  status: '',
  profile: {username: '', email: '', name: '', is_manager: false, is_upper_manager: false},
  allReviewNotes: []
};

export default state;
