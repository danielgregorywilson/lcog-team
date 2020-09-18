import http from '../http-common';

class PerformanceReviewDataService {
  getAll() {
    return http.get('api/v1/performancereview/');
  }

  getAllManagerUpcomingActionRequired() {
    return http.get('api/v1/performancereview/?action_required=True');
  }

  getAllManagerUpcomingNoActionRequired() {
    return http.get('api/v1/performancereview/?action_required=False');
  }

  getAllUpperManagerUpcomingActionRequired() {
    return http.get('api/v1/performancereview/?action_required=True&upper_manager=True');
  }

  getAllUpperManagerUpcomingNoActionRequired() {
    return http.get('api/v1/performancereview/?action_required=False&upper_manager=True');
  }

  get(pk) {
    return http.get(`api/v1//performancereview/{${parseInt(pk, 10)}}`);
  }

  create(data) {
    return http.post('api/v1//performancereview', data);
  }

  update(pk, data) {
    return http.put(`api/v1//performancereview/${parseInt(pk, 10)}`, data);
  }

  delete(pk) {
    return http.delete(`api/v1//performancereview/${parseInt(pk, 10)}`);
  }

  deleteAll() {
    return http.delete('api/v1//performancereview');
  }

  findByTitle(title) {
    return http.get(`api/v1//performancereview?title=${title}`);
  }
}

export default new PerformanceReviewDataService();
