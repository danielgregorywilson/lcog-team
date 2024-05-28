import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import {
  Desk, DeskReservation, DeskReservationCreate,
  GetDeskSummaryReportDataInterface, GetDetailReportDataInterface,
  GetEmployeeSummaryReportDataInterface, GetReservationReportData
} from 'src/types'

export const useDeskReservationStore = defineStore('deskreservation', {
  state: () => ({
    allDesks: [] as Array<Desk>,
    allDeskReservations: [] as Array<DeskReservation>,
  }),

  getters: {},

  actions: {
    createReservation(data: DeskReservationCreate): Promise<DeskReservation> {
      return new Promise((resolve, reject) => {
        axios(
          { url: `${ apiURL }api/v1/deskreservation`, method: 'POST', data }
        )
          .then((resp) => {
            resolve(resp.data)
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
        axios({
          url: `${ apiURL }api/v1/deskreservation/${pk}/cancel-reservation`,
          method: 'PUT'
        })
          .then((resp) => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error cancelling desk reservation', e)
          })
      })
    },
    getDeskSummaryReport(
      data: GetReservationReportData
    ): Promise<GetDeskSummaryReportDataInterface> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/deskreservation/desk-summary-report`,
          method: 'POST',
          data
        })
          .then((resp) => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating desk summary report', e)
          })
      })
    },
    getDeskDetailReport(
      data: GetReservationReportData
    ): Promise<GetDetailReportDataInterface> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/deskreservation/desk-detail-report`,
          method: 'POST',
          data
        })
          .then((resp) => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating desk detail report', e)
          })
      })
    },
    getEmployeeSummaryReport(
      data: GetReservationReportData
    ): Promise<GetEmployeeSummaryReportDataInterface> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/deskreservation/employee-summary-report`,
          method: 'POST',
          data
        })
          .then((resp) => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error creating employee summary report', e
            )
          })
      })
    },
    getEmployeeDetailReport(
      data: GetReservationReportData
    ): Promise<GetDetailReportDataInterface> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/deskreservation/employee-detail-report`,
          method: 'POST',
          data
        })
          .then((resp) => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error creating employee detail report', e
            )
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
