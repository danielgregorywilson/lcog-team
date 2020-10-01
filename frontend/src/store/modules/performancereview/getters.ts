import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';

const getters: GetterTree<PerformanceReviewStateInterface, StateInterface> = {
  allReviewNotes: state => state.allReviewNotes
};

export default getters;
