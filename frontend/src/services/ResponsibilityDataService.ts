import http from '../http-common';
import { ResponsibilityUpdate } from 'src/store/types';


class ResponsibilityDataService {
  getAll() {
    return http.get('api/v1/responsibilities');
  }

  getOrphaned() {
    return http.get('api/v1/responsibilities?orphaned=True');
  }

  getPrimariesForEmployee(employee_pk: number) {
    return http.get(`api/v1/responsibilities?employee=${employee_pk}`)
  }

  getSecondariesForEmployee(employee_pk: number) {
    return http.get(`api/v1/responsibilities?employee=${employee_pk}&secondary=True`)
  }

  update(pk: string, data: ResponsibilityUpdate) {
    return http.put(`api/v1/responsibilities/${pk}`, data);
  }
}

export default new ResponsibilityDataService();
