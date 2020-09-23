import http from '../http-common';

import { PerformanceReview } from '../store/types'

class PerformanceReviewDataService {
  getAll() {
    return http.get('api/v1/performancereview');
  }

  getAllManagerUpcomingActionRequired() {
    return http.get('api/v1/performancereview?action_required=True');
  }

  getAllManagerUpcomingNoActionRequired() {
    return http.get('api/v1/performancereview?action_required=False');
  }

  getAllUpperManagerUpcomingActionRequired() {
    return http.get('api/v1/performancereview?action_required=True&upper_manager=True');
  }

  getAllUpperManagerUpcomingNoActionRequired() {
    return http.get('api/v1/performancereview?action_required=False&upper_manager=True');
  }

  get(pk: number) {
    return http.get(`api/v1/performancereview/${pk}`);
  }

  create(data: PerformanceReview) {
    return http.post('api/v1/performancereview', data);
  }

  update(pk: number, data: PerformanceReview) {
    return http.put(`api/v1/performancereview/${pk}`, data);
  }

  delete(pk: number) {
    return http.delete(`api/v1/performancereview/${pk}`);
  }

  deleteAll() {
    return http.delete('api/v1/performancereview');
  }

  findByTitle(title: string) {
    return http.get(`api/v1/performancereview?title=${title}`);
  }
}

export default new PerformanceReviewDataService();
