import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import {
  PerformanceReviewRetrieve, ReviewNoteCreate, ReviewNoteRetrieve,
  SignatureCreate
} from 'src/types'

export const usePerformanceReviewStore = defineStore('performancereview', {
  state: () => ({
    nextPerformanceReview: {} as PerformanceReviewRetrieve,
    // performanceReview: [] as Array<Responsibility>,
    performanceReviewDetails: {} as PerformanceReviewRetrieve,
    allPerformanceReviews: [] as Array<PerformanceReviewRetrieve>,
    allPerformanceReviewsActionRequired: [] as Array<PerformanceReviewRetrieve>,
    allPerformanceReviewsActionNotRequired: [] as
      Array<PerformanceReviewRetrieve>,
    allSignaturePerformanceReviewsActionRequired: [] as
      Array<PerformanceReviewRetrieve>,
    allSignaturePerformanceReviewsActionNotRequired: [] as
      Array<PerformanceReviewRetrieve>,
    allReviewNotes: [] as Array<ReviewNoteRetrieve>
  }),

  getters: {},

  actions: {
    getNextPerformanceReview(data: {pk: number}) {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/employee/${data.pk}/` +
            'employee_next_performance_review',
          method: 'POST'
        })
          .then(resp => {
            this.nextPerformanceReview = resp.data
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting next performance review', e
            )
          })
      })
    },
    getAllReviewNotes() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/reviewnote` })
          .then(resp => {
            this.allReviewNotes = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting all review notes', e)
          })
      })
    },
    createReviewNote(reviewNote: ReviewNoteCreate) {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/reviewnote`,
          data: reviewNote,
          method: 'POST'
        })
          .then(() => {
            this.getAllReviewNotes()
              .then(() => {
                resolve('Successfully created a review note')
              })
              .catch(e => {
                handlePromiseError(
                  reject,
                  'Error getting all review notes ater creating a review note',
                  e
                )
              })
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating a review note', e)
          })
      })
    },
    createSignature({}, signature: SignatureCreate) {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/signature`, data: signature, method: 'POST'
        })
          .then(() => {
            resolve('Successfully created a signature')
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating a signature', e)
          })
      })
    },
    getPerformanceReview(data: {pk: number}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/performancereview/${ data.pk }` })
          .then(resp => {
            this.performanceReviewDetails = resp.data
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting performance review', e)
          })
      })
    },
    // All performance reviews for your direct reports and their descendants
    getAllPerformanceReviews(data: {signature: boolean}) {
      return new Promise((resolve, reject) => {
        let targetUrl: string
        if (data.signature) {
          targetUrl = `${ apiURL }api/v1/performancereview?signature=true`
        } else {
          targetUrl = `${ apiURL }api/v1/performancereview`
        }
        axios({ url: targetUrl })
          .then(resp => {
            this.allPerformanceReviews = resp.data
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting all performance reviews', e
            )
          })
      })
    },
    getAllPerformanceReviewsActionRequired() {
      return new Promise((resolve, reject) => {
        axios(
          { url: `${ apiURL }api/v1/performancereview?action_required=True` }
        )
          .then(resp => {
            this.allPerformanceReviewsActionRequired = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting all performance reviews action required', e
            )
          })
      })
    },
    getAllPerformanceReviewsActionNotRequired() {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/performancereview?action_required=False`
        })
          .then(resp => {
            this.allPerformanceReviewsActionNotRequired = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(
              reject,
              'Error getting all performance reviews action not required',
              e
            )
          })
      })
    },
    getAllSignaturePerformanceReviewsActionRequired() {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/performancereview?signature=True` +
            '&action_required=True'
        })
          .then(resp => {
            this.allSignaturePerformanceReviewsActionRequired = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting all signature PRs action required', e
            )
          })
      })
    },
    getAllSignaturePerformanceReviewsActionNotRequired() {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/performancereview?signature=True` +
            '&action_required=False'
        })
          .then(resp => {
            this.allSignaturePerformanceReviewsActionNotRequired = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting all signature PRs action not required', e
            )
          })
      })
    },

    //////////////////
    // Review Notes //
    //////////////////

    deleteReviewNote(pk: number) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/reviewnote/${ pk }`, method: 'DELETE' })
          .then(() => {
            this.getAllReviewNotes()
              .then(() => {
                resolve('Successfully deleted a review note')
              })
              .catch(e => {
                handlePromiseError(
                  reject,
                  'Error getting all review notes after deleting a review note',
                  e
                )
              })
          })
          .catch(e => {
            handlePromiseError(reject, 'Error deleting a review note', e)
          })
      })
    },

    // TODO: Still needed?
    // updatePerformanceReview: ({ dispatch }, performanceReview: PerformanceReviewUpdate) => {
    //   const token = localStorage.getItem('user-token')
    //   console.log('TODO:UPDATE')
    //   return new Promise((resolve, reject) => {
    //     debugger
    //     axios({ url: `${ apiURL }api/v1/performancereview/${performanceReview.pk}`, data: performanceReview, method: 'PUT', headers: { 'Authorization': `Token ${ token }`} }) // eslint-disable-line
    //     .then(resp => {
    //       dispatch('getAllPerformanceReviews')
    //         .catch(e => {
    //           console.error(e)
    //         })
    //       resolve(resp)
    //     })
    //     .catch(e => {
    //       console.error(e)
    //       reject(e)
    //     })
    //   })
    // },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        resolve('Successfully triggered logout')
      })
    },
  }
})
