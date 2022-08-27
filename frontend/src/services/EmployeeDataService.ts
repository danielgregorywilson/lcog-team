import http from '../http-common';

import { EmployeeUpdatePartial } from '../store/types'


class EmployeeDataService {
  getAll() {
    return http.get('api/v1/employee');
  }

  getDirectReports() {
    return http.get('api/v1/employee?direct-reports=True');
  }

  // getProfile(pk: number) {
  //   return http.get(`api/v1/employee/${pk}/get_profile`)
  // }

  // For updating employee profile
  updatePartial(pk: number, data: EmployeeUpdatePartial) {
    return http.patch(`api/v1/employee/${pk}`, data)
  }

  getEmployeeNextPerformanceReview(pk: number) {
    return http.get(`api/v1/employee/${pk}/employee_next_performance_review`)
  }
}

export default new EmployeeDataService();
