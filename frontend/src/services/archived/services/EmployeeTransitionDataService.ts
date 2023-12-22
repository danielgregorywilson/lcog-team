import http from '../http-common';

import { EmployeeTransitionUpdate } from '../store/types'


class EmployeeTransitionDataService {
  // getAll() {
  //   return http.get('api/v1/reviewnote');
  // }

  // get(pk: string) {
  //   return http.get(`api/v1/reviewnote/${pk}`);
  // }

  // getAllManagerNotesForEmployee(pk: number) {
  //   return http.get(`api/v1/reviewnote/${pk}/notes_for_employee`)
  // }

  // create(data: ReviewNoteCreate) {
  //   return http.post('api/v1/reviewnote', data);
  // }

  update(pk: string, data: EmployeeTransitionUpdate) {
    return http.put(`api/v1/employeetransition/${pk}`, data);
  }

  // delete(pk: string) {  //   return http.delete(`api/v1/workflowinstance/${pk}`);
  // }

  // deleteAll() {
  //   return http.delete('api/v1/reviewnote');
  // }

  // findByTitle(title: string) {
  //   return http.get(`api/v1/reviewnote?title=${title}`);
  // }
}

export default new EmployeeTransitionDataService();
