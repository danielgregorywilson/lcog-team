export interface AuthStateInterface {
  token: string;
  status: string;
}

const state: AuthStateInterface = {
  token: localStorage.getItem('user-token') || '',
  status: ''
};

export default state;
