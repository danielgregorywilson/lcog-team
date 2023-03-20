import axios from 'axios';
import { defineStore } from 'pinia';
import { 
  TimeOffRequestAcknowledge, TimeOffRequestCreate, TimeOffRequestDates,
  TimeOffRequestStateInterface
} from 'src/types';
import { useUserStore } from './user';

const userStore = useUserStore()

const apiURL = process.env.API_URL ?
  process.env.API_URL : 'https://api.team.lcog.org/'

export const useTimeOffStore = defineStore('timeoff', {
  state: (): TimeOffRequestStateInterface => ({
    myTimeOffRequests: [],
    teamTimeOffRequests: [],
    managedTimeOffRequests: [],
    conflictingTimeOffRequests: []
  }),

  getters: {},

  actions: {
    getMyTimeOffRequests() {
      axios({ url: `${ apiURL }api/v1/timeoffrequest` })
        .then(resp => {
          this.myTimeOffRequests = resp.data
        })
        .catch(e => {
          console.log(e)
        });
    },
    getTeamTimeOffRequests() {
      axios({ url: `${ apiURL }api/v1/timeoffrequest?team=True` })
        .then(resp => {
          this.teamTimeOffRequests = resp.data
        })
        .catch(e => {
          console.log(e)
        });
    },
    getManagedTimeOffRequests() {
      axios({ url: `${ apiURL }api/v1/timeoffrequest?managed=True` })
        .then(resp => {
          this.managedTimeOffRequests = resp.data
        })
        .catch(e => {
          console.log(e)
        });
    },
    getConflictingResponsibilities(data: { dates: Array<TimeOffRequestDates>}) {
      axios({ url: `${ apiURL }api/v1/timeoffrequest/conflicting_responsibilities`, data: data, method: 'POST' })
        .then(resp => {
          this.conflictingTimeOffRequests = resp.data
        })
        .catch(e => {
          console.log(e)
        });
    },
    createTimeOffRequest(timeOffRequest: TimeOffRequestCreate) {
      axios({ url: `${ apiURL }api/v1/timeoffrequest`, data: timeOffRequest, method: 'POST' })
        .then(() => {
          this.getMyTimeOffRequests()
          userStore.userRequest()
            .catch(err => console.log(err))
        })
        .catch(e => {
          console.log(e)
        });
    },
    acknowledgeTimeOffRequest(timeOffRequest: TimeOffRequestAcknowledge) {
      axios({ url: `${ apiURL }api/v1/timeoffrequest`, data: timeOffRequest, method: 'PUT' })
        .then(() => {
          this.getMyTimeOffRequests()
        })
        .catch(e => {
          console.log(e)
        });
    },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        resolve('Successfully triggered logout')
      })
    }
  }
});
