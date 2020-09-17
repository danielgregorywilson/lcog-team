import http from '../http-common';

class ReviewNoteDataService {
  getAll() {
    return http.get('api/v1/reviewnote/');
  }

  get(pk) {
    return http.get(`api/v1//reviewnote/{${parseInt(pk, 10)}}`);
  }

  create(data) {
    return http.post('api/v1//reviewnote', data);
  }

  update(pk, data) {
    return http.put(`api/v1//reviewnote/${parseInt(pk, 10)}`, data);
  }

  delete(pk) {
    return http.delete(`api/v1//reviewnote/${parseInt(pk, 10)}`);
  }

  deleteAll() {
    return http.delete('api/v1//reviewnote');
  }

  findByTitle(title) {
    return http.get(`api/v1//reviewnote?title=${title}`);
  }
}

export default new ReviewNoteDataService();