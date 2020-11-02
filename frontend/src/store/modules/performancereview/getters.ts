import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';

const getters: GetterTree<PerformanceReviewStateInterface, StateInterface> = {
  nextPerformanceReview: state => state.nextPerformanceReview,
  allReviewNotes: state => state.allReviewNotes,
  performanceReview: state => state.performanceReview,
  performanceReviewDetails: state => state.performanceReviewDetails, // TODO: Use this instead of performanceReview
  allPerformanceReviews: state => state.allPerformanceReviews,
  allPerformanceReviewsActionRequired: state => state.allPerformanceReviewsActionRequired,
  allPerformanceReviewsActionNotRequired: state => state.allPerformanceReviewsActionNotRequired,
  allUpperManagerPerformanceReviewsActionRequired: state => state.allUpperManagerPerformanceReviewsActionRequired,
  allUpperManagerPerformanceReviewsActionNotRequired: state => state.allUpperManagerPerformanceReviewsActionNotRequired,
};

export default getters;
