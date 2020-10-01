import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';

const getters: GetterTree<PerformanceReviewStateInterface, StateInterface> = {
  allReviewNotes: state => state.allReviewNotes,
  allPerformanceReviewsActionRequired: state => state.allPerformanceReviewsActionRequired,
  allPerformanceReviewsActionNotRequired: state => state.allPerformanceReviewsActionNotRequired
};

export default getters;
