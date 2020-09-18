export interface ProfileInterface {
  name: ''
}

export interface UserStateInterface {
  status: string;
  profile: ProfileInterface;
}

const state: UserStateInterface = {
  status: '',
  profile: {name: ''}
};

export default state;
