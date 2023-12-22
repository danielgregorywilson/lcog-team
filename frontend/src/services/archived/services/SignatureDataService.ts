import http from '../http-common';

import { SignatureCreate } from '../store/types'


class SignatureDataService {
  getAll() {
    return http.get('api/v1/signature');
  }

  get(pk: string) {
    return http.get(`api/v1/signature/${pk}`);
  }

  create(data: SignatureCreate) {
    return http.post('api/v1/signature', data);
  }

  delete(pk: string) {
    return http.delete(`api/v1/signature/${pk}`);
  }

  deleteAll() {
    return http.delete('api/v1/signature');
  }
}

export default new SignatureDataService();
