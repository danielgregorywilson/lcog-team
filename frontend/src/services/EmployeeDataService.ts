import http from '../http-common';

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

  updateProfile(pk: number) {
    return http.get(`api/v1/employee/${pk}/update_profile`)
  }

  getEmployeeNextPerformanceReview(pk: number) {
    return http.get(`api/v1/employee/${pk}/employee_next_performance_review`)
  }
}

export default new EmployeeDataService();
