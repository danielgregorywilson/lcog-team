import TimeOffRequest from 'src/pages/timeoff/NewRequest.vue';
import { PerformanceReviewRetrieve, ReviewNoteRetrieve } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { TimeOffRequestStateInterface } from './state'


const mutation: MutationTree<TimeOffRequestStateInterface> = {
  setMyTimeOffRequests: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'myTimeOffRequests', resp.data)
  },
  setTeamTimeOffRequests: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'teamTimeOffRequests', resp.data)
  },
  setManagedTimeOffRequests: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'managedTimeOffRequests', resp.data)
  },
  setConflictingResponsibilities: (state, resp: {data: Array<TimeOffRequest>}) => {
    Vue.set(state, 'conflictingTimeOffRequests', resp.data)
  },

  
  setAllReviewNotes: (state, resp: {data: Array<ReviewNoteRetrieve>}) => {
    Vue.set(state, 'allReviewNotes', resp.data)
  },
  setPerformanceReview: (state, resp: {data: PerformanceReviewRetrieve}) => {
    Vue.set(state, 'performanceReview', resp.data)
  },
  setAllPerformanceReviews: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allPerformanceReviews', resp.data)
  },
  setAllPerformanceReviewsActionRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allPerformanceReviewsActionRequired', resp.data)
  },
  setAllPerformanceReviewsActionNotRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allPerformanceReviewsActionNotRequired', resp.data)
  },
  setAllSignaturePerformanceReviewsActionRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allSignaturePerformanceReviewsActionRequired', resp.data)
  },
  setAllSignaturePerformanceReviewsActionNotRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allSignaturePerformanceReviewsActionNotRequired', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.myTimeOffRequests = []
    
    // state.nextPerformanceReview = {pk: undefined, employee_pk: undefined, employee_name: '', performance_period: '', days_until_review: '', status: '', evaluation: ''}
    // state.performanceReview = {pk: undefined, employee_pk: undefined, employee_name: '', performance_period: '', days_until_review: '', status: '', evaluation: ''}
    // state.allPerformanceReviews = []
    // state.allPerformanceReviewsActionRequired = []
    // state.allPerformanceReviewsActionNotRequired = []
    // state.allSignaturePerformanceReviewsActionRequired = []
    // state.allSignaturePerformanceReviewsActionNotRequired = []
    // state.performanceReviewDetails = {}
    // state.allReviewNotes = []
  }
};

export default mutation;
