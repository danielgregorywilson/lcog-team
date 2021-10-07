import { EmployeeRetrieve } from 'src/store/types';
import Vue from 'vue';

import { MutationTree } from 'vuex';
import { UserStateInterface } from './state';


const mutation: MutationTree<UserStateInterface> = {
  userRequest: (state) => {
    state.status = 'loading'
  },
  userSuccess: (state, resp: {data: EmployeeRetrieve}) => {
    state.status = 'success'
    Vue.set(state, 'profile', resp.data)
    Vue.prototype.$cookies.set('is_manager', resp.data.is_manager) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$cookies.set('has_manager', resp.data.has_manager) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$cookies.set('is_eligible_for_telework_application', resp.data.is_eligible_for_telework_application) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$cookies.set('can_view_seating_charts', resp.data.can_view_seating_charts) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$cookies.set('can_edit_seating_charts', resp.data.can_edit_seating_charts) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$cookies.set('prs_can_view', resp.data.prs_can_view) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$cookies.set('notes_can_view', resp.data.notes_can_view) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$cookies.set('telework_applications_can_view', resp.data.telework_applications_can_view) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  },
  userError: (state) => {
    state.status = 'error'
  },
  authLogout: (state) => {
    // Clean up state
    state.profile = {employee_pk: -1, username: '', email: '', name: '', is_manager: false, has_manager: false, is_eligible_for_telework_application: false, can_view_seating_charts: false, can_edit_seating_charts: false, is_upper_manager: false, is_hr_manager: false, is_executive_director: false, viewed_security_message: false, prs_can_view: [], notes_can_view: [], telework_applications_can_view: [], next_to_sign_prs: ''}
    Vue.prototype.$cookies.remove('is_manager') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    Vue.prototype.$cookies.remove('has_manager') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    Vue.prototype.$cookies.remove('is_eligible_for_telework_application') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    Vue.prototype.$cookies.remove('can_view_seating_charts') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    Vue.prototype.$cookies.remove('can_edit_seating_charts') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    Vue.prototype.$cookies.remove('prs_can_view') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    Vue.prototype.$cookies.remove('notes_can_view') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    Vue.prototype.$cookies.remove('telework_applications_can_view') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
  }
};

export default mutation;
