import http from '../http-common';

import { PerformanceReviewCreate, PerformanceReviewUpdate, PerformanceReviewUpdatePartial } from '../store/types'

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

  getAllSignatureUpcomingActionRequired() {
    return http.get('api/v1/performancereview?action_required=True&signature=True');
  }

  getAllSignatureUpcomingNoActionRequired() {
    return http.get('api/v1/performancereview?action_required=False&signature=True');
  }

  get(pk: string) {
    return http.get(`api/v1/performancereview/${pk}`);
  }

  create(data: PerformanceReviewCreate) {
    return http.post('api/v1/performancereview', data);
  }

  update(pk: string, data: PerformanceReviewUpdate) {
    return http.put(`api/v1/performancereview/${pk}`, data);
  }

  updatePartial(pk: string, data: PerformanceReviewUpdatePartial) {
    return http.patch(`api/v1/performancereview/${pk}`, data);
  }

  uploadSignedPositionDescription(data: FormData) {
    return http.post('api/v1/fileupload', data)
  }

  signPerformanceReview(performanceReviewPk: number, employeePk: number) {
    return http.put(`api/v1/performancereview/${performanceReviewPk}/sign/${employeePk}`)
  }

  delete(pk: string) {
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
