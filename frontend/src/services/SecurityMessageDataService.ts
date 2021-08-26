import http from '../http-common';

import { ReviewNoteCreate, ReviewNoteUpdate } from '../store/types'


class SecurityMessageDataService {
  getAll() {
    return http.get('api/v1/securitymessage');
  }

  get(pk: string) {
    return http.get(`api/v1/securitymessage/${pk}`);
  }

  getLatestSecurityMessage() {
    return http.get(`api/v1/securitymessage/get_latest_security_message`)
  }

  // create(data: ReviewNoteCreate) {
  //   return http.post('api/v1/reviewnote', data);
  // }

  // update(pk: string, data: ReviewNoteUpdate) {
  //   return http.put(`api/v1/reviewnote/${pk}`, data);
  // }

  // delete(pk: string) {
  //   return http.delete(`api/v1/reviewnote/${pk}`);
  // }

  // deleteAll() {
  //   return http.delete('api/v1/reviewnote');
  // }

  // findByTitle(title: string) {
  //   return http.get(`api/v1/reviewnote?title=${title}`);
  // }
}

export default new SecurityMessageDataService();
