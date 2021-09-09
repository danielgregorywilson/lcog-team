import http from '../http-common';

import { TeleworkApplicationCreate, TeleworkApplicationUpdate, TeleworkApplicationUpdatePartial } from '../store/types'

class TeleworkApplicationDataService {
  // TODO: Remove unneeded service methods
  getAll() {
    return http.get('api/v1/teleworkapplication');
  }

  getAllSignatureUpcomingActionRequired() {
    return http.get('api/v1/teleworkapplication?action_required=True&signature=True');
  }

  getAllSignatureUpcomingNoActionRequired() {
    return http.get('api/v1/teleworkapplication?action_required=False&signature=True');
  }

  get(pk: string) {
    return http.get(`api/v1/teleworkapplication/${pk}`);
  }

  create(data: TeleworkApplicationCreate) {
    return http.post('api/v1/teleworkapplication', data);
  }

  update(pk: string, data: TeleworkApplicationUpdate) {
    return http.put(`api/v1/teleworkapplication/${pk}`, data);
  }

  updatePartial(pk: string, data: TeleworkApplicationUpdatePartial) {
    return http.patch(`api/v1/teleworkapplication/${pk}`, data);
  }

  uploadDependentCareDocumentation(data: FormData) {
    return http.post('api/v1/telework-fileupload', data)
  }

  signTeleworkApplication(teleworkApplicationPk: number, employeePk: number) {
    return http.put(`api/v1/teleworkapplication/${teleworkApplicationPk}/sign/${employeePk}`)
  }

  delete(pk: string) {
    return http.delete(`api/v1/teleworkapplication/${pk}`);
  }

  deleteAll() {
    return http.delete('api/v1/teleworkapplication');
  }
}

export default new TeleworkApplicationDataService();
