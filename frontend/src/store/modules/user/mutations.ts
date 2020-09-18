import Vue from 'vue';

import { MutationTree } from 'vuex';
import { UserStateInterface } from './state';


const mutation: MutationTree<UserStateInterface> = {
  userRequest: (state) => {
    state.status = 'loading'
  },
  userSuccess: (state, resp) => {
    state.status = 'success';
    Vue.set(state, 'profile', resp);
  },
  userError: (state) => {
    state.status = 'error'
  },
  authLogout: (state) => {
    state.profile = {name: ''}
  }
};

export default mutation;
