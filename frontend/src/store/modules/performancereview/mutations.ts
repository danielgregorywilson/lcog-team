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
  setPerformanceReviewDetail: (state, resp: {data: PerformanceReviewRetrieve}) => {
    debugger
    Vue.set(state, 'performanceReviewDetails', resp.data)
  },
  setAllPerformanceReviewsActionRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allPerformanceReviewsActionRequired', resp.data)
  },
  setAllPerformanceReviewsActionNotRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allPerformanceReviewsActionNotRequired', resp.data)
  },
};

export default mutation;
