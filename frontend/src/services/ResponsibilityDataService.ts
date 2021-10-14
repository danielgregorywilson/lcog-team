import http from '../http-common';

class ResponsibilityDataService {
  getAll() {
    return http.get('api/v1/responsibility');
  }

  getOrphaned() {
    return http.get('api/v1/responsibility?orphaned=True');
  }

  getPrimariesForEmployee(employee_pk: number) {
    return http.get(`api/v1/responsibility?employee=${employee_pk}`)
  }

  getSecondariesForEmployee(employee_pk: number) {
    return http.get(`api/v1/responsibility?employee=${employee_pk}&secondary=True`)
  }
}

export default new ResponsibilityDataService();
