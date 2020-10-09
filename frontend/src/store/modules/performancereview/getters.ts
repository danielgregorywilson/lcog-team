import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';

const getters: GetterTree<PerformanceReviewStateInterface, StateInterface> = {
  nextPerformanceReview: state => state.nextPerformanceReview,
  allReviewNotes: state => state.allReviewNotes,
  performanceReviewDetails: state => state.performanceReviewDetails,
  allPerformanceReviewsActionRequired: state => state.allPerformanceReviewsActionRequired,
  allPerformanceReviewsActionNotRequired: state => state.allPerformanceReviewsActionNotRequired
};

export default getters;
