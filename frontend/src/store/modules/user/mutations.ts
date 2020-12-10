import { EmployeeRetrieve } from 'src/store/types';
import Vue from 'vue';

import { MutationTree } from 'vuex';
import { UserStateInterface } from './state';


const mutation: MutationTree<UserStateInterface> = {
  userRequest: (state) => {
    state.status = 'loading'
  },
  userSuccess: (state, resp: {data: EmployeeRetrieve}) => {
    state.status = 'success';
    Vue.set(state, 'profile', resp.data);
  },
  userError: (state) => {
    state.status = 'error'
  },
  authLogout: (state) => {
    // Clean up state
    state.profile = {employee_pk: -1, username: '', email: '', name: '', is_manager: false, is_upper_manager: false, is_hr_manager: false, is_executive_director: false, prs_can_view: [], notes_can_view: []}
  }
};

export default mutation;
