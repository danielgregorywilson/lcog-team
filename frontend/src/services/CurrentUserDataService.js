import http from '../http-common';

class CurrentUserDataService {
  get() {
    return http.get('api/v1/current-user/');
  }
}

export default new CurrentUserDataService();
