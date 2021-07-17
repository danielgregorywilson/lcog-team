import { MutationTree } from 'vuex';
import { AuthStateInterface } from './state';

const mutation: MutationTree<AuthStateInterface> = {
  // Old way of logging in via /auth/login
  authRequest: state => {
    state.status = 'loading'
  },
  // Log in with Microsoft Azure SSO
  setAuth: state => {
    state.status = 'loading'
  },
  authSuccess: (state, token: string) => {
    state.status = 'success'
    state.token = token
  },
  authError: state => {
    state.status = 'error'
  },
  authLogout: state => {
    // Clean up state
    state.token = '';
  }
};

export default mutation;
