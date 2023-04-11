import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import {
  AxiosDeskReservationCreateServerResponse, Desk, DeskReservation,
  DeskReservationCreate
} from 'src/types'

export const useDeskReservationStore = defineStore('deskreservation', {
  state: () => ({
    allDesks: [] as Array<Desk>,
    allDeskReservations: [] as Array<DeskReservation>,
  }),

  getters: {},

  actions: {
    createReservation(data: DeskReservationCreate): Promise<AxiosDeskReservationCreateServerResponse> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/deskreservation`, method: 'POST', data })
          .then((resp) => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating desk reservation', e)
          })
      })
    },
    getAllDesks() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/desk` })
          .then(resp => {
            this.allDesks = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting all desks', e)
          })
      })
    },
    getAllDeskReservations() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/deskreservation` })
          .then(resp => {
            this.allDeskReservations = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting all desk reservations', e)
          })
      })
    },
    cancelReservation(pk: number) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/deskreservation/${pk}/cancel-reservation`, method: 'PUT' })
          .then((resp) => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error cancelling desk reservation', e)
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
