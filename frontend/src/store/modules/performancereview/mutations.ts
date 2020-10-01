import { PerformanceReviewRetrieve, ReviewNoteRetrieve } from 'src/store/types';
import Vue from 'vue';

import { MutationTree } from 'vuex';
import { PerformanceReviewStateInterface } from './state';


const mutation: MutationTree<PerformanceReviewStateInterface> = {
  setAllReviewNotes: (state, resp: {data: Array<ReviewNoteRetrieve>}) => {
    Vue.set(state, 'allReviewNotes', resp.data);
  },
  setAllPerformanceReviewsActionRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allPerformanceReviewsActionRequired', resp.data);
  },
  setAllPerformanceReviewsActionNotRequired: (state, resp: {data: Array<PerformanceReviewRetrieve>}) => {
    Vue.set(state, 'allPerformanceReviewsActionNotRequired', resp.data);
  },
};

export default mutation;
