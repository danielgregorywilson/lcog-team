import http from '../http-common';

class EmployeeDataService {
  getAll() {
    return http.get('api/v1/employee/');
  }

  getDirectReports() {
    return http.get('api/v1/employee/?direct-reports=True');
  }
}

export default new EmployeeDataService();
