import { EmployeeRetrieve, ReviewNoteRetrieve } from 'src/store/types';
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
    state.profile = {username: '', email: '', name: '', is_manager: false, is_upper_manager: false}
  },
  setAllReviewNotes: (state, resp: {data: Array<ReviewNoteRetrieve>}) => {
    Vue.set(state, 'allReviewNotes', resp.data);
  },
};

export default mutation;
