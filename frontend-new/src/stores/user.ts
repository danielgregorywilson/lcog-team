import { defineStore } from 'pinia';
import { Stop, AxiosAuthResponse, UserRetrieve } from 'src/types';
import axios from 'axios';

// TODO
// const apiURL = process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/'
const apiURL = 'http://lcog-team:8000/'

export const useUserStore = defineStore('user', {
  state: () => ({
    status: '',
    profile: {
      employee_pk: -1,
      username: '',
      email: '',
      name: '',
      is_manager: false,
      has_manager: false,
      is_eligible_for_telework_application: false,
      can_view_seating_charts: false,
      can_edit_seating_charts: false,
      is_upper_manager: false,
      is_hr_manager: false,
      is_executive_director: false,
      viewed_security_message: false,
      prs_can_view: [],
      notes_can_view: [],
      telework_applications_can_view: [],
      time_off_requests_can_view: [],
      next_to_sign_prs: '',
      workflow_roles: [],
      can_view_mow_routes: false,
      can_manage_mow_stops: false
    }
  }),

  getters: {
    getEmployeeProfile: state => state.profile,
    isProfileLoaded: state => !!state.profile.name,
    isManager: state => state.profile.is_manager,
    hasWorkflowRoles: state => !!state.profile.workflow_roles.length,
    canViewMOWRoutes: state => state.profile.can_view_mow_routes,
    canManageMOWStops: state => state.profile.can_manage_mow_stops
  },

  actions: {
    // For requesting user on login
    userRequest() {
      return new Promise((resolve, reject) => {
        this.status = 'loading';
        axios({ url: `${ process.env.API_URL }api/v1/current-user/` })
          .then((resp: {data: {pk: number}}) => {
            commit('userSuccess', resp);
            // TODO: Convert this
            // dispatch('performanceReviewModule/getNextPerformanceReview', {pk: resp.data.pk}, { root: true })
            //   .catch(err => console.log(err))
            // dispatch('securityMessageModule/getViewedLatestSecurityMessage', {}, { root: true })
            //   .catch(err => console.log(err))
            resolve(resp)
          })
          .catch(e => {
            this.status = 'error';
            // if resp is unauthorized, logout, to
            this.authLogout()
              .catch(err => console.log(err))
            reject(e)
          });
      })
    },
    // For getting just the user on specific pages
    simpleUserRequest: () => {
      return new Promise((resolve, reject) => {
        axios({ url: `${ process.env.API_URL }api/v1/current-user/` })
          .then((resp: {data: {pk: number}}) => {
            resolve(resp)
          })
          .catch(e => {
            reject(e)
          });
      })
    },
    authLogout: () => {
      return new Promise((resolve) => {
        commit('authLogout')
        resolve('Successfully triggered logout')
      })
    }
  }
});
