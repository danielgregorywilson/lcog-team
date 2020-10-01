import { ReviewNoteRetrieve } from 'src/store/types';
import Vue from 'vue';

import { MutationTree } from 'vuex';
import { PerformanceReviewStateInterface } from './state';


const mutation: MutationTree<PerformanceReviewStateInterface> = {
  setAllReviewNotes: (state, resp: {data: Array<ReviewNoteRetrieve>}) => {
    Vue.set(state, 'allReviewNotes', resp.data);
  },
};

export default mutation;
