import axios from 'axios';
import { defineStore } from 'pinia';
import { 
  TimeOffRequestAcknowledge, TimeOffRequestCreate, TimeOffRequestDates,
  TimeOffRequestRetrieve, TimeOffRequestStateInterface,
  TimeOffRequestUpdate
} from 'src/types';
import { useUserStore } from './user';

const userStore = useUserStore()

const apiURL = process.env.API_URL ?
  process.env.API_URL : 'https://api.team.lcog.org/'

export const useTimeOffStore = defineStore('timeoff', {
  state: (): TimeOffRequestStateInterface => ({
    myTimeOffRequests: [],
    currentTimeOffRequest: {} as TimeOffRequestRetrieve,
    teamTimeOffRequests: [],
    managedTimeOffRequests: [],
    conflictingTimeOffRequests: [] as Array<TimeOffRequestRetrieve>
  }),

  getters: { },

  actions: {
    getMyTimeOffRequests() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/timeoffrequest` })
          .then(resp => {
            this.myTimeOffRequests = resp.data.results
            resolve('Successfully got my time off requests')
          })
          .catch(e => {
            console.log(e)
            reject('Error getting my time off requests')
          });
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
            console.log(e)
            reject('Error getting team time off requests')
          });
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
            console.log(e)
            reject('Error getting managed time off requests')
          });
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
            console.log(e)
            reject('Error getting conflicting responsibilities')
          });
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
            console.log(e)
            reject('Error getting current time off request')
          });
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
            console.log(e)
            reject('Error creating time off request')
          });
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
            console.log(e)
            reject('Error updating time off request')
          });
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
            console.log(e)
            reject('Error acknowledging time off request')
          });
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
            console.log(e)
            reject('Error deleting time off request')
          });
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
