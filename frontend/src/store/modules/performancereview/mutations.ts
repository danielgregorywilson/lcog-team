import { PerformanceReviewRetrieve, ReviewNoteRetrieve } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { PerformanceReviewStateInterface } from './state'


const mutation: MutationTree<PerformanceReviewStateInterface> = {
  setNextPerformanceReview: (state, resp: {data: PerformanceReviewRetrieve}) => {
    Vue.set(state, 'nextPerformanceReview', resp.data)
  },
  employeeMarkDiscussed: (state) => {
    state.nextPerformanceReview.employee_marked_discussed = true
  },
  setAllReviewNotes: (state, resp: {data: Array<ReviewNoteRetrieve>}) => {
    Vue.set(state, 'allReviewNotes', resp.data)
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
  setAllUpperManagerPerformanceReviewsActionRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allUpperManagerPerformanceReviewsActionRequired', resp.data)
  },
  setAllUpperManagerPerformanceReviewsActionNotRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allUpperManagerPerformanceReviewsActionNotRequired', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.nextPerformanceReview = {pk: undefined, employee_pk: undefined, employee_name: '', date_of_review: '', days_until_review: '', status: '', date_of_discussion: '', evaluation: '', employee_marked_discussed: false, discussion_took_place: false}
    state.allPerformanceReviews = []
    state.allPerformanceReviewsActionRequired = []
    state.allPerformanceReviewsActionNotRequired = []
    state.allUpperManagerPerformanceReviewsActionRequired = []
    state.allUpperManagerPerformanceReviewsActionNotRequired = []
    state.performanceReviewDetails = {}
    state.allReviewNotes = []
  }
};

export default mutation;
