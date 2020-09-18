import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { AuthStateInterface } from './state';

const getters: GetterTree<AuthStateInterface, StateInterface> = {
  isAuthenticated: state => !!state.token,
  authStatus: state => state.status
};

export default getters;
