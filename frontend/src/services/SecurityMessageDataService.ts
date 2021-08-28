import http from '../http-common';


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

  hasViewedLatestSecurityMessage(): boolean {
    return http.get(`api/v1/viewedsecuritymessage/employee_viewed_latest_security_message`)
  }
}

export default new SecurityMessageDataService();
