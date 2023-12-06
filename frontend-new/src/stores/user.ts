import axios from 'axios'
import { defineStore } from 'pinia'
import { useCookies } from 'vue3-cookies'

import { apiURL, handlePromiseError } from 'src/stores/index'
import { useSecurityMessageStore } from 'src/stores/securitymessage'
import {
  ClientError, EmployeeRetrieve, SimpleEmployeeRetrieve
} from 'src/types'

const { cookies } = useCookies()

export const useUserStore = defineStore('user', {
  state: () => ({
    status: '',
    profile: {
      employee_pk: -1,
      username: '',
      email: '',
      name: '',
      division: '',
      is_manager: false,
      has_manager: false,
      is_is_employee: false,
      is_hr_employee: false,
      is_sds_hiring_lead: false,
      is_fiscal_employee: false,
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
      is_all_workflows_admin: false,
      can_view_expenses: false,
      can_view_mow_routes: false,
      can_manage_mow_stops: false
    },
    simpleEmployeeList: [] as Array<SimpleEmployeeRetrieve>,
    simpleEmployeeDetail: { pk: -1, name: '' } as SimpleEmployeeRetrieve,
  }),

  getters: {
    getEmployeeProfile: state => state.profile,
    isProfileLoaded: state => !!state.profile.username,
    isManager: state => state.profile.is_manager,
    hasWorkflowRoles: state => !!state.profile.workflow_roles.length,
    canViewExpenses: state => state.profile.can_view_expenses,
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
            this.profile.employee_pk = resp.data.pk
            this.profile.username = resp.data.username
            this.profile.email = resp.data.email
            this.profile.name = resp.data.name
            this.profile.division = resp.data.division
            this.profile.is_manager = resp.data.is_manager
            this.profile.has_manager = resp.data.has_manager
            this.profile.is_is_employee = resp.data.is_is_employee
            this.profile.is_hr_employee = resp.data.is_hr_employee
            this.profile.is_sds_hiring_lead = resp.data.is_sds_hiring_lead
            this.profile.is_fiscal_employee = resp.data.is_fiscal_employee
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
            this.profile.is_all_workflows_admin = resp.data.is_all_workflows_admin
            this.profile.can_view_expenses = resp.data.can_view_expenses
            this.profile.can_view_mow_routes = resp.data.can_view_mow_routes
            this.profile.can_manage_mow_stops = resp.data.can_manage_mow_stops
            cookies.set('division', resp.data.division.toString())
            cookies.set('is_manager', resp.data.is_manager.toString())
            cookies.set('has_manager', resp.data.has_manager.toString())
            cookies.set('is_is_employee', resp.data.is_is_employee.toString())
            cookies.set('is_hr_employee', resp.data.is_hr_employee.toString())
            cookies.set('is_sds_hiring_lead', resp.data.is_sds_hiring_lead.toString())
            cookies.set('is_fiscal_employee', resp.data.is_fiscal_employee.toString())
            cookies.set('is_eligible_for_telework_application', resp.data.is_eligible_for_telework_application.toString())
            cookies.set('can_view_seating_charts', resp.data.can_view_seating_charts.toString())
            cookies.set('can_edit_seating_charts', resp.data.can_edit_seating_charts.toString())
            cookies.set('prs_can_view', resp.data.prs_can_view.toString())
            cookies.set('notes_can_view', resp.data.notes_can_view.toString())
            cookies.set('telework_applications_can_view', resp.data.telework_applications_can_view.toString())
            cookies.set('time_off_requests_can_view', resp.data.time_off_requests_can_view.toString())
            cookies.set('workflow_roles', resp.data.workflow_roles.toString())
            cookies.set('can_view_expenses', resp.data.can_view_expenses.toString())
            cookies.set('can_view_mow_routes', resp.data.can_view_mow_routes.toString())
            cookies.set('can_manage_mow_stops', resp.data.can_manage_mow_stops.toString())

            // TODO: Convert this
            // dispatch('performanceReviewModule/getNextPerformanceReview', {pk: resp.data.pk}, { root: true })
            //   .catch(err => console.log(err))
            const securityMessageStore = useSecurityMessageStore()
            securityMessageStore.getViewedLatestSecurityMessage()
              .catch(err => console.log(err))
            resolve(resp)
          })
          .catch(e => {
            this.status = 'error'
            // if resp is unauthorized, logout, to
            this.authLogout()
              .catch(err => console.log(err))
            reject(e)
          })
      })
    },
    // For getting just the current user on specific pages
    simpleUserRequest: (): Promise<EmployeeRetrieve> => {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/current-user/` })
          .then(resp => resolve(resp.data))
          .catch(e => handlePromiseError(
            reject, 'Error getting current user', e
          ))
      })
    },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        cookies.remove('division')
        cookies.remove('is_manager')
        cookies.remove('has_manager')
        cookies.remove('is_is_employee')
        cookies.remove('is_hr_employee')
        cookies.remove('is_sds_hiring_lead')
        cookies.remove('is_fiscal_employee')
        cookies.remove('is_eligible_for_telework_application')
        cookies.remove('can_view_seating_charts')
        cookies.remove('can_edit_seating_charts')
        cookies.remove('prs_can_view')
        cookies.remove('notes_can_view')
        cookies.remove('telework_applications_can_view')
        cookies.remove('time_off_requests_can_view')
        cookies.remove('workflow_roles')
        cookies.remove('can_view_expenses')
        cookies.remove('can_view_mow_routes')
        cookies.remove('can_manage_mow_stops')
        resolve('Successfully triggered logout')
      })
    },
    // Log a frontend error in AWS CloudWatch
    // TODO: This doesn't belong here, but I don't have a generic utility store.
    logError(data: ClientError) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/log-error`, data, method: 'POST' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error logging error LOL:', e)
          })
      })
    },

    // TODO: More stuff that doesn't belong here: Zoom test create meetings
    // Authenticate a Zoom user
    // TODO: Unused
    getZoomAuthorizationToken() {
      return new Promise((resolve, reject) => {
        axios({ url: 'https://zoom.us/oauth/authorize?response_type=code&client_id=PFvjFxQERmqeMKlaJ_R4g&redirect_uri=https://team-staging.lcog.org/', data: {  }, method: 'GET' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error authenticating Zoom user: requesting user authoriation:', e)
          })
      })
    },

    // Authenticate a Zoom user
    getZoomAccessToken(authorizationCode: string) {
      return new Promise((resolve, reject) => {
        const client_id = 'PFvjFxQERmqeMKlaJ_R4g'
        const client_secret = 'C6uv4I1k4vOfSgnJktUKCSrD4hJMKgUs'
        const encodedString = btoa(`${ client_id }:${ client_secret }`)
        axios({ url: `${ apiURL }api/v1/zoom-access-token/` })
          .then(resp => resolve(resp.data))
          .catch(e => handlePromiseError(
            reject, 'Error getting Zoom access token', e
          ))



        axios({
          url: 'https://zoom.us/oauth/token',
          data: {
            grant_type: 'authorization_code',
            code: authorizationCode,
            redirect_uri: 'https://team-staging.lcog.org/'
          },
          method: 'POST',
          headers: {
            'Authorization': `Basic ${ encodedString }`,
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
          .then(resp => {
            console.log(resp)
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error authenticating Zoom user: requesting access token', e)
          })
      })
    },

    // Create a Zoom meeting link
    createZoomMeeting(userId: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `https://api.zoom.us/v2/users/${userId}/meetings`, data: { }, method: 'POST' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating Zoom meeting link:', e)
          })
      })
    },
  }
})
