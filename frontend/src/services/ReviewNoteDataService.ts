import http from '../http-common';

import { ReviewNote } from '../store/types'


class ReviewNoteDataService {
  getAll() {
    return http.get('api/v1/reviewnote/');
  }

  get(pk: number) {
    return http.get(`api/v1//reviewnote/{${pk}}`);
  }

  create(data: ReviewNote) {
    return http.post('api/v1//reviewnote', data);
  }

  update(pk: number, data: ReviewNote) {
    return http.put(`api/v1//reviewnote/${pk}`, data);
  }

  delete(pk: number) {
    return http.delete(`api/v1//reviewnote/${pk}`);
  }

  deleteAll() {
    return http.delete('api/v1//reviewnote');
  }

  findByTitle(title: string) {
    return http.get(`api/v1//reviewnote?title=${title}`);
  }
}

export default new ReviewNoteDataService();
