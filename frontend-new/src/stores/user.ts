import { defineStore } from 'pinia';
import { EmployeeRetrieve, SimpleEmployeeRetrieve } from 'src/types';
import axios from 'axios';
import { useCookies } from 'vue3-cookies'

const apiURL = process.env.API_URL ?
  process.env.API_URL : 'https://api.team.lcog.org/'

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
      prs_can_view: [] as Array<number>,
      notes_can_view: [] as Array<number>,
      telework_applications_can_view: [] as Array<number>,
      time_off_requests_can_view: [] as Array<number>,
      next_to_sign_prs: '',
      workflow_roles: [] as Array<number>,
      can_view_mow_routes: false,
      can_manage_mow_stops: false
    },
    simpleEmployeeList: [] as Array<SimpleEmployeeRetrieve>,
    simpleEmployeeDetail: { pk: -1, name: '' } as SimpleEmployeeRetrieve,
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
        this.status = 'loading'
        axios({ url: `${ apiURL }api/v1/current-user/` })
          .then((resp: {data: EmployeeRetrieve}) => {
            this.status = 'success'
            const { cookies } = useCookies()
            this.profile.employee_pk = resp.data.pk
            this.profile.username = resp.data.username
            this.profile.email = resp.data.email
            this.profile.name = resp.data.name
            this.profile.is_manager = resp.data.is_manager
            this.profile.has_manager = resp.data.has_manager
            this.profile.is_eligible_for_telework_application = resp.data.is_eligible_for_telework_application
            this.profile.can_view_seating_charts = resp.data.can_view_seating_charts
            this.profile.can_edit_seating_charts = resp.data.can_edit_seating_charts
            this.profile.is_upper_manager = resp.data.is_upper_manager
            this.profile.is_hr_manager = resp.data.is_hr_manager
            this.profile.is_executive_director = resp.data.is_executive_director
            this.profile.viewed_security_message = resp.data.viewed_security_message
            this.profile.prs_can_view = resp.data.prs_can_view
            this.profile.notes_can_view = resp.data.notes_can_view
            this.profile.telework_applications_can_view = resp.data.telework_applications_can_view
            this.profile.time_off_requests_can_view = resp.data.time_off_requests_can_view
            this.profile.next_to_sign_prs = resp.data.next_to_sign_prs
            this.profile.workflow_roles = resp.data.workflow_roles
            this.profile.can_view_mow_routes = resp.data.can_view_mow_routes
            this.profile.can_manage_mow_stops = resp.data.can_manage_mow_stops
            cookies.set('is_manager', resp.data.is_manager.toString())
            cookies.set('has_manager', resp.data.has_manager.toString())
            cookies.set('is_eligible_for_telework_application', resp.data.is_eligible_for_telework_application.toString())
            cookies.set('can_view_seating_charts', resp.data.can_view_seating_charts.toString())
            cookies.set('can_edit_seating_charts', resp.data.can_edit_seating_charts.toString())
            cookies.set('prs_can_view', resp.data.prs_can_view.toString())
            cookies.set('notes_can_view', resp.data.notes_can_view.toString())
            cookies.set('telework_applications_can_view', resp.data.telework_applications_can_view.toString())
            cookies.set('time_off_requests_can_view', resp.data.time_off_requests_can_view.toString())
            cookies.set('workflow_roles', resp.data.workflow_roles.toString())
            cookies.set('can_view_mow_routes', resp.data.can_view_mow_routes.toString())
            cookies.set('can_manage_mow_stops', resp.data.can_manage_mow_stops.toString())

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
    // For getting just the current user on specific pages
    simpleUserRequest: () => {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/current-user/` })
          .then((resp: {data: {pk: number}}) => resolve(resp))
          .catch(e => reject(e));
      })
    },
    // Simple list of all employees
    getSimpleEmployeeList() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/employee/simple_list`})
          .then(resp => {
            this.simpleEmployeeList = resp.data
            resolve('Got simple employee list')
          })
          .catch(e => {
            console.error('Error getting simple employee list:', e)
            reject(`Error getting simple employee list: ${ e }`)
          })
      })
    },
    // Simple detail of one employee
    getSimpleEmployeeDetail(data: {pk: number}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/employee/${ data.pk }/simple_detail`})
          .then(resp => {
            this.simpleEmployeeDetail = resp.data
            resolve('Got simple employee detail')
          })
          .catch(e => {
            console.error('Error getting simple employee detail:', e)
            reject(`Error getting simple employee detail: ${ e }`)
          })
      })
    },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        resolve('Successfully triggered logout')
      })
    }
  }
});
