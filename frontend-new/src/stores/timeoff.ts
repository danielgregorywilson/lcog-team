import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import { useUserStore } from 'src/stores/user'
import { 
  TimeOffRequestAcknowledge, TimeOffRequestCreate, TimeOffRequestDates,
  TimeOffRequestRetrieve, TimeOffRequestUpdate
} from 'src/types'

const userStore = useUserStore()

export const useTimeOffStore = defineStore('timeoff', {
  state: () => ({
    myTimeOffRequests: [] as Array<TimeOffRequestRetrieve>,
    currentTimeOffRequest: {} as TimeOffRequestRetrieve,
    teamTimeOffRequests: [] as Array<TimeOffRequestRetrieve>,
    managedTimeOffRequests: [] as Array<TimeOffRequestRetrieve>,
    conflictingTimeOffRequests: [] as Array<TimeOffRequestRetrieve>
  }),

  getters: {},

  actions: {
    getMyTimeOffRequests() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest` })
          .then(resp => {
            this.myTimeOffRequests = resp.data.results
            resolve('Successfully got my time off requests')
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting my time off requests', e)
          })
      })
    },
    getTeamTimeOffRequests() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest?team=True` })
          .then(resp => {
            this.teamTimeOffRequests = resp.data.results
            resolve('Successfully got team time off requests')
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting team time off requests', e
            )
          })
      })
    },
    getManagedTimeOffRequests() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest?managed=True` })
          .then(resp => {
            this.managedTimeOffRequests = resp.data.results
            resolve('Successfully got managed time off requests')
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting managed time off requests', e
            )
          })
      })
    },
    getConflictingTimeOffRequests(data: { dates: TimeOffRequestDates}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest/conflicting_responsibilities`, data: data, method: 'POST' })
          .then(resp => {
            this.conflictingTimeOffRequests = resp.data.results
            resolve('Successfully got conflicting responsibilities')
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting conflicting responsibilities', e
            )
          })
      })
    },
    getCurrentTimeOffRequest(pk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest/${ pk }` })
          .then(resp => {
            this.currentTimeOffRequest = resp.data
            resolve('Successfully got current time off request')
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting current time off request', e
            )
          })
      })
    },
    createTimeOffRequest(timeOffRequest: TimeOffRequestCreate) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest`, data: timeOffRequest, method: 'POST' })
          .then(() => {
            this.getMyTimeOffRequests()
            userStore.userRequest()
              .catch(err => console.log(err))
            resolve('Successfully created time off request')
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating time off request', e)
          })
      })
    },
    updateTimeOffRequest(data: TimeOffRequestUpdate) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest/${ data.pk }`, data, method: 'PUT' })
          .then(() => {
            this.getMyTimeOffRequests()
            userStore.userRequest()
              .catch(err => console.log(err))
            resolve('Successfully updated time off request')
          })
          .catch(e => {
            handlePromiseError(reject, 'Error updating time off request', e)
          })
      })
    },
    acknowledgeTimeOffRequest(data: TimeOffRequestAcknowledge) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest/${ data.pk }`, data, method: 'PATCH' })
          .then(() => {
            this.getMyTimeOffRequests()
            resolve('Successfully acknowledged time off request')
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error acknowledging time off request', e
            )
          })
      })
    },
    deleteTimeOffRequest(pk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest/${ pk }`, method: 'DELETE' })
          .then(() => {
            this.getMyTimeOffRequests()
            resolve('Successfully deleted time off request')
          })
          .catch(e => {
            handlePromiseError(reject, 'Error deleting time off request', e)
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
})
